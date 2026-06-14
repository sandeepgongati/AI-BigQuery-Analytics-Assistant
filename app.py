import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.grok_helper import ask_grok

from src.uploaded_file_analytics import (
    load_file,
    get_basic_stats
)
from src.analytics import (
    total_sales,
    total_orders,
    top_city,
    top_product,
    top_revenue_cities,
    top_products,
    monthly_sales,
    average_order_value,
    total_products,
    top_orders
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Intelligence · Sandeep Gongati",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL THEME
# --------------------------------------------------

CHART_COLORS = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#4f46e5"]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
    title_font=dict(family="Inter, sans-serif", color="#f1f5f9", size=16),
    xaxis=dict(gridcolor="#1e293b", linecolor="#334155", tickfont=dict(color="#64748b")),
    yaxis=dict(gridcolor="#1e293b", linecolor="#334155", tickfont=dict(color="#64748b")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=dict(bgcolor="#1e293b", font_color="#f1f5f9", bordercolor="#334155")
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.main .block-container {
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid #1e293b;
}

/* Page header */
.dash-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 1.5rem 0 1rem 0;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 1.8rem;
}
.dash-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
    letter-spacing: -0.02em;
}
.dash-header p {
    color: #64748b;
    font-size: 0.82rem;
    margin: 0.25rem 0 0 0;
}
.dash-badge {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* Insight cards (replace KPI grid - uses st.columns instead) */
.kpi-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-top: 2px solid #6366f1;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
}
.kpi-icon  { font-size: 1.1rem; margin-bottom: 0.5rem; display: block; }
.kpi-label { font-size: 0.68rem; font-weight: 600; color: #475569;
             text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.kpi-value { font-size: 1.4rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }

/* Insight row cards */
.insight-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-left: 3px solid #6366f1;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
}
.insight-label { font-size: 0.68rem; text-transform: uppercase;
                 letter-spacing: 0.08em; color: #6366f1; font-weight: 600; margin-bottom: 0.3rem; }
.insight-value { font-size: 0.95rem; color: #e2e8f0; font-weight: 500; }

/* Upload stat grid */
.upload-stat {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.u-val   { font-size: 1.4rem; font-weight: 700; color: #a5b4fc; }
.u-label { font-size: 0.68rem; text-transform: uppercase;
           letter-spacing: 0.07em; color: #475569; margin-top: 0.2rem; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #1e293b;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent;
    color: #64748b;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 0.6rem 1rem;
    border: none;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #1e293b !important;
    color: #a5b4fc !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.55rem 1.4rem !important;
}
.stDownloadButton > button {
    background: transparent !important;
    color: #6366f1 !important;
    border: 1px solid #312e81 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}

/* Text area */
.stTextArea textarea {
    background: #0a0f1e !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus { border-color: #6366f1 !important; }

/* AI chat messages */
.chat-user {
    background: #1e293b;
    border-radius: 10px 10px 2px 10px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    color: #e2e8f0;
    font-size: 0.85rem;
    text-align: right;
}
.chat-ai {
    background: #0f0f23;
    border: 1px solid #312e81;
    border-radius: 10px 10px 10px 2px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    color: #94a3b8;
    font-size: 0.85rem;
    line-height: 1.6;
}
.chat-label-user { font-size: 0.65rem; color: #475569; text-align: right; margin-bottom: 0.2rem; }
.chat-label-ai   { font-size: 0.65rem; color: #6366f1; margin-bottom: 0.2rem; }

/* AI panel wrapper */
.ai-panel-wrap {
    background: linear-gradient(135deg, #0f0f23, #0f172a);
    border: 1px solid #312e81;
    border-radius: 14px;
    padding: 1.25rem 1.5rem 1.5rem 1.5rem;
    margin-top: 1rem;
}
.ai-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #6366f1;
    border-radius: 50%;
    box-shadow: 0 0 8px #6366f1;
    margin-right: 0.5rem;
    vertical-align: middle;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: #334155;
    font-size: 0.75rem;
    border-top: 1px solid #1e293b;
    margin-top: 2rem;
}

/* Section label */
.sec-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #94a3b8;
    margin-bottom: 0.6rem;
    letter-spacing: -0.01em;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def apply_chart_theme(fig, title=""):
    fig.update_layout(**PLOTLY_LAYOUT)
    if title:
        fig.update_layout(title_text=title)
    return fig


# FIX 1: KPI cards via st.columns (not st.markdown grid)
# This is what caused the raw HTML display — Streamlit sandboxes
# complex CSS grid inside markdown. We use real columns instead.
def render_kpi(col, icon, label, value):
    col.markdown(
        f'<div class="kpi-card">'
        f'<span class="kpi-icon">{icon}</span>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_insight(col, label, value):
    col.markdown(
        f'<div class="insight-box">'
        f'<div class="insight-label">{label}</div>'
        f'<div class="insight-value">{value}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1.5rem 0;'>
        <div style='font-size:1.1rem;font-weight:700;color:#f1f5f9;'>📊 Retail Intelligence</div>
        <div style='font-size:0.72rem;color:#475569;margin-top:0.2rem;'>AI-Powered Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    data_source = st.radio(
        "Data Source",
        ["BigQuery Analytics", "Upload CSV/Excel"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;color:#334155;line-height:1.8;'>
        Stack: Python · BigQuery<br>
        Streamlit · Plotly · Grok AI<br>
        Google Cloud Platform
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE — chat histories
# --------------------------------------------------

if "bq_chat" not in st.session_state:
    st.session_state.bq_chat = []      # [{role, text}]

if "upload_chat" not in st.session_state:
    st.session_state.upload_chat = []  # [{role, text}]

# --------------------------------------------------
# UPLOAD MODE
# --------------------------------------------------

if data_source == "Upload CSV/Excel":

    st.markdown("""
    <div class="dash-header">
        <div><h1>Dataset Explorer</h1>
        <p>Upload a CSV or Excel file for instant AI-powered analysis</p></div>
        <div class="dash-badge">Upload Mode</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV or Excel", type=["csv", "xlsx"]
    )

    if uploaded_file:

        df_raw = load_file(uploaded_file)
        stats  = get_basic_stats(df_raw)

        # Upload stat cards via columns
        uc1, uc2, uc3, uc4 = st.columns(4)
        for col, val, lbl in [
            (uc1, f"{stats['rows']:,}",         "Rows"),
            (uc2, str(stats['columns']),         "Columns"),
            (uc3, str(stats['missing_values']),  "Missing Values"),
            (uc4, str(stats['duplicates']),      "Duplicates"),
        ]:
            col.markdown(
                f'<div class="upload-stat"><div class="u-val">{val}</div>'
                f'<div class="u-label">{lbl}</div></div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Arrow-safe copy for display
        df = df_raw.astype(str)

        tab_prev, tab_cols, tab_stats, tab_ai = st.tabs([
            "📋 Data Preview", "🗂 Column Info", "📐 Statistics", "🤖 AI Analyst"
        ])

        # ── Preview tab ──
        with tab_prev:
            st.markdown('<div class="sec-label">First 20 rows</div>', unsafe_allow_html=True)
            st.dataframe(df.head(20), use_container_width=True, height=420)

        # ── Column tab ──
        with tab_cols:
            st.markdown('<div class="sec-label">Column Schema</div>', unsafe_allow_html=True)
            st.dataframe(
                pd.DataFrame({
                    "Column":       df.columns,
                    "Data Type":    df.dtypes.astype(str),
                    "Non-Null":     df_raw.notnull().sum().values,
                    "Unique Values":df_raw.nunique().values
                }),
                use_container_width=True,
                height=420
            )

        # ── Stats tab ──
        with tab_stats:
            st.markdown('<div class="sec-label">Descriptive Statistics</div>', unsafe_allow_html=True)
            st.dataframe(df_raw.describe(), use_container_width=True, height=280)

            numeric_cols = df_raw.select_dtypes(include="number").columns.tolist()

            if numeric_cols:
                st.markdown("<br>", unsafe_allow_html=True)
                selected_col = st.selectbox("Visualize column", numeric_cols)

                # FIX 2: Default to bar chart — much more readable than histogram
                # for typical business datasets with categorical grouping
                value_counts = (
                    df_raw[selected_col]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"index": selected_col, "count": "Count"})
                    .head(30)
                )

                # If too many unique values, fall back to histogram
                unique_vals = df_raw[selected_col].nunique()

                if unique_vals <= 30:
                    fig = go.Figure(go.Bar(
                        x=value_counts[selected_col].astype(str),
                        y=value_counts["Count"],
                        marker=dict(
                            color=value_counts["Count"],
                            colorscale=[[0,"#312e81"],[0.5,"#6366f1"],[1,"#a78bfa"]],
                            showscale=False,
                            line=dict(color="#4f46e5", width=0.5)
                        ),
                        text=value_counts["Count"],
                        textposition="outside",
                        textfont=dict(color="#94a3b8", size=11),
                        hovertemplate=f"{selected_col}: %{{x}}<br>Count: %{{y}}<extra></extra>"
                    ))
                    fig = apply_chart_theme(fig, f"Value Distribution — {selected_col}")
                    fig.update_layout(xaxis_title=selected_col, yaxis_title="Count", height=400)
                else:
                    fig = go.Figure(go.Histogram(
                        x=df_raw[selected_col],
                        nbinsx=40,
                        marker=dict(
                            color="#6366f1",
                            line=dict(color="#4f46e5", width=0.5)
                        ),
                        hovertemplate=f"{selected_col}: %{{x}}<br>Count: %{{y}}<extra></extra>"
                    ))
                    fig = apply_chart_theme(fig, f"Distribution — {selected_col}")
                    fig.update_layout(xaxis_title=selected_col, yaxis_title="Count", height=400)

                st.plotly_chart(fig, use_container_width=True)

        # ── AI Analyst tab with persistent chat ──
        with tab_ai:

            st.markdown("""
            <div class="ai-panel-wrap">
                <div style="margin-bottom:1rem;">
                    <span class="ai-dot"></span>
                    <span style="font-size:0.9rem;font-weight:600;color:#e2e8f0;">AI Dataset Analyst</span>
                    <div style="font-size:0.72rem;color:#64748b;margin-top:0.25rem;margin-left:1.1rem;">
                        Powered by Grok · Chat history saved for this session
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # FIX 3: Render saved chat history
            for msg in st.session_state.upload_chat:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-label-user">You</div>'
                        f'<div class="chat-user">{msg["text"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="chat-label-ai">🤖 Grok</div>'
                        f'<div class="chat-ai">{msg["text"]}</div>',
                        unsafe_allow_html=True
                    )

            dataset_question = st.text_area(
                "Ask about this dataset",
                placeholder="e.g. What are the key trends? Which column has the most missing data?",
                height=90,
                label_visibility="visible",
                key="upload_q"
            )

            col_btn, col_clear = st.columns([2, 1])
            with col_btn:
                ask_clicked = st.button("Analyze with Grok", key="upload_ask")
            with col_clear:
                if st.button("Clear Chat", key="upload_clear"):
                    st.session_state.upload_chat = []
                    st.rerun()

            if ask_clicked and dataset_question.strip():
                # Build chat context from history
                history_ctx = "\n".join([
                    f"{'User' if m['role']=='user' else 'Grok'}: {m['text']}"
                    for m in st.session_state.upload_chat[-6:]  # last 3 exchanges
                ])

                prompt = f"""
You are a professional data analyst in an ongoing conversation.

Dataset Columns: {list(df.columns)}
Sample Data (first 20 rows):
{df.head(20).to_string()}

Statistical Summary:
{df_raw.describe().to_string()}

Previous conversation:
{history_ctx}

Current Question: {dataset_question}

Give a clear, structured, business-focused answer. Use bullet points where helpful.
"""
                with st.spinner("Grok is thinking..."):
                    response = ask_grok(prompt)

                st.session_state.upload_chat.append({"role": "user",      "text": dataset_question})
                st.session_state.upload_chat.append({"role": "assistant", "text": response})
                st.rerun()

    else:
        st.info("👆 Upload a CSV or Excel file from the sidebar to get started.")

    st.stop()

# --------------------------------------------------
# BIGQUERY DASHBOARD
# --------------------------------------------------

sales        = total_sales()[0]["total_sales"]
orders       = total_orders()[0]["total_orders"]
avg_order    = average_order_value()[0]["avg_order_value"]
products     = total_products()[0]["total_products"]
best_city    = top_city()[0]
best_product = top_product()[0]

# Header
st.markdown("""
<div class="dash-header">
    <div>
        <h1>Retail Intelligence Dashboard</h1>
        <p>Real-time analytics powered by Google BigQuery & Grok AI</p>
    </div>
    <div class="dash-badge">● Live · BigQuery</div>
</div>
""", unsafe_allow_html=True)

# FIX 1: KPI cards rendered via st.columns — no more raw HTML dump
k1, k2, k3, k4, k5, k6 = st.columns(6)
render_kpi(k1, "💰", "Total Revenue",    f"${sales:,}")
render_kpi(k2, "📦", "Total Orders",     f"{orders:,}")
render_kpi(k3, "🌎", "Top City",         best_city["city"])
render_kpi(k4, "🏆", "Top Product",      best_product["product"])
render_kpi(k5, "🛒", "Avg Order Value",  f"${avg_order:,.2f}")
render_kpi(k6, "📋", "Products",         str(products))

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌆  Revenue by City",
    "📦  Revenue by Product",
    "📈  Monthly Trend",
    "🎯  Top Orders"
])

# TAB 1
with tab1:
    data = pd.DataFrame(top_revenue_cities())
    col_chart, col_table = st.columns([3, 2], gap="large")

    with col_chart:
        fig = go.Figure(go.Bar(
            x=data["city"], y=data["total_revenue"],
            marker=dict(
                color=data["total_revenue"],
                colorscale=[[0,"#312e81"],[0.5,"#6366f1"],[1,"#a78bfa"]],
                showscale=False, line=dict(color="#4f46e5", width=0.5)
            ),
            text=data["total_revenue"].apply(lambda v: f"${v:,}"),
            textposition="outside", textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,}<extra></extra>"
        ))
        fig = apply_chart_theme(fig, "Revenue by City")
        fig.update_layout(xaxis_title="", yaxis_title="Revenue (USD)")
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown('<div class="sec-label">City Breakdown</div>', unsafe_allow_html=True)
        st.dataframe(
            data.rename(columns={"city":"City","total_revenue":"Revenue ($)"}),
            use_container_width=True, height=320, hide_index=True
        )
        st.download_button("📥 Export CSV", data.to_csv(index=False), "city_revenue.csv", "text/csv")

# TAB 2
with tab2:
    data = pd.DataFrame(top_products())
    col_chart, col_table = st.columns([3, 2], gap="large")

    with col_chart:
        fig = go.Figure(go.Pie(
            labels=data["product"], values=data["total_revenue"],
            hole=0.55,
            marker=dict(colors=CHART_COLORS, line=dict(color="#0f172a", width=2)),
            textfont=dict(color="#e2e8f0", size=12),
            hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,}<br>Share: %{percent}<extra></extra>"
        ))
        fig = apply_chart_theme(fig, "Revenue Distribution by Product")
        fig.update_layout(
            annotations=[dict(text=f"${sales:,}", x=0.5, y=0.5,
                              font_size=16, font_color="#f1f5f9",
                              font_family="Inter", showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown('<div class="sec-label">Product Breakdown</div>', unsafe_allow_html=True)
        st.dataframe(
            data.rename(columns={"product":"Product","total_revenue":"Revenue ($)"}),
            use_container_width=True, height=320, hide_index=True
        )
        st.download_button("📥 Export CSV", data.to_csv(index=False), "product_revenue.csv", "text/csv")

# TAB 3
with tab3:
    data = pd.DataFrame(monthly_sales())
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["month"], y=data["total_revenue"],
        mode="lines+markers",
        line=dict(color="#6366f1", width=2.5),
        marker=dict(size=7, color="#a78bfa", line=dict(color="#6366f1", width=1.5)),
        fill="tozeroy", fillcolor="rgba(99,102,241,0.08)",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,}<extra></extra>"
    ))
    fig = apply_chart_theme(fig, "Monthly Revenue Trend")
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (USD)", height=400)
    st.plotly_chart(fig, use_container_width=True)

    col_t, col_d = st.columns([3, 1])
    with col_t:
        st.dataframe(
            data.rename(columns={"month":"Month","total_revenue":"Revenue ($)"}),
            use_container_width=True, hide_index=True
        )
    with col_d:
        st.download_button("📥 Export CSV", data.to_csv(index=False), "monthly_sales.csv", "text/csv")

# TAB 4
with tab4:
    data = pd.DataFrame(top_orders())
    fig = go.Figure(go.Bar(
        x=data["order_id"].astype(str), y=data["revenue"],
        marker=dict(
            color=data["revenue"],
            colorscale=[[0,"#312e81"],[0.5,"#6366f1"],[1,"#a78bfa"]],
            showscale=False
        ),
        text=data["revenue"].apply(lambda v: f"${v:,}"),
        textposition="outside", textfont=dict(color="#94a3b8", size=10),
        hovertemplate="Order: %{x}<br>Revenue: $%{y:,}<extra></extra>"
    ))
    fig = apply_chart_theme(fig, "Top Revenue Orders")
    fig.update_layout(xaxis_title="Order ID", yaxis_title="Revenue (USD)", height=380)
    st.plotly_chart(fig, use_container_width=True)

    col_t, col_d = st.columns([3, 1])
    with col_t:
        st.dataframe(data, use_container_width=True, hide_index=True)
    with col_d:
        st.download_button("📥 Export CSV", data.to_csv(index=False), "top_orders.csv", "text/csv")

# --------------------------------------------------
# BUSINESS SNAPSHOT
# --------------------------------------------------

st.markdown("---")
st.markdown('<div class="sec-label" style="margin-bottom:0.8rem;">📈 Business Snapshot</div>', unsafe_allow_html=True)

ic1, ic2, ic3, ic4 = st.columns(4)
render_insight(ic1, "Highest Revenue City",  best_city["city"])
render_insight(ic2, "Best Selling Product",  best_product["product"])
render_insight(ic3, "Average Order Value",   f"${avg_order:,.2f}")
render_insight(ic4, "Total Products",        str(products))

# --------------------------------------------------
# AI ASSISTANT — BigQuery chat with history
# --------------------------------------------------

st.markdown("---")
st.markdown("""
<div class="ai-panel-wrap">
    <span class="ai-dot"></span>
    <span style="font-size:0.9rem;font-weight:600;color:#e2e8f0;">Grok AI Data Analyst</span>
    <div style="font-size:0.72rem;color:#64748b;margin-top:0.25rem;margin-left:1.1rem;">
        Ask anything about your business · Chat history saved for this session
    </div>
</div>
""", unsafe_allow_html=True)

# FIX 3: Render BigQuery chat history
for msg in st.session_state.bq_chat:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-label-user">You</div>'
            f'<div class="chat-user">{msg["text"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-label-ai">🤖 Grok</div>'
            f'<div class="chat-ai">{msg["text"]}</div>',
            unsafe_allow_html=True
        )

question = st.text_area(
    "Your question",
    placeholder="e.g. Why is New York the top city? How can we grow Boston revenue?",
    height=90,
    label_visibility="collapsed",
    key="bq_q"
)

col_ask, col_clr = st.columns([2, 1])
with col_ask:
    ask_bq = st.button("Ask Grok AI", key="bq_ask")
with col_clr:
    if st.button("Clear Chat", key="bq_clear"):
        st.session_state.bq_chat = []
        st.rerun()

if ask_bq and question.strip():
    history_ctx = "\n".join([
        f"{'User' if m['role']=='user' else 'Grok'}: {m['text']}"
        for m in st.session_state.bq_chat[-6:]
    ])

    prompt = f"""
You are an expert retail business analyst in an ongoing conversation.

Dashboard Metrics:
- Total Revenue: ${sales:,}
- Total Orders: {orders:,}
- Top City: {best_city['city']}
- Top Product: {best_product['product']}
- Average Order Value: ${avg_order:,.2f}
- Total Products: {products}

Previous conversation:
{history_ctx}

Current Question: {question}

Give a detailed, actionable, business-focused answer. Use bullet points and clear sections where helpful.
"""
    with st.spinner("Grok is thinking..."):
        response = ask_grok(prompt)

    st.session_state.bq_chat.append({"role": "user",      "text": question})
    st.session_state.bq_chat.append({"role": "assistant", "text": response})
    st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    <strong style="color:#64748b;">Retail Intelligence Dashboard</strong> &nbsp;·&nbsp;
    Built with Python, BigQuery, Streamlit, Plotly &
    <span style="color:#6366f1;">Grok AI</span><br>
    <span style="color:#334155;">© 2026 Sandeep Gongati · All Rights Reserved</span>
</div>
""", unsafe_allow_html=True)