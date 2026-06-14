from src.bigquery_helper import run_query


def top_revenue_cities():
    query = """
    SELECT
        city,
        SUM(revenue) AS total_revenue
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    GROUP BY city
    ORDER BY total_revenue DESC
    """
    return run_query(query)


def top_products():
    query = """
    SELECT
        product,
        SUM(revenue) AS total_revenue
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    GROUP BY product
    ORDER BY total_revenue DESC
    """
    return run_query(query)


def monthly_sales():
    query = """
    SELECT
        FORMAT_DATE('%Y-%m', order_date) AS month,
        SUM(revenue) AS total_revenue
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    GROUP BY month
    ORDER BY month
    """
    return run_query(query)


def total_sales():
    query = """
    SELECT
        SUM(revenue) AS total_sales
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    """
    return run_query(query)
def total_orders():
    query = """
    SELECT COUNT(*) AS total_orders
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    """
    return run_query(query)


def top_city():
    query = """
    SELECT city,
           SUM(revenue) AS revenue
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    GROUP BY city
    ORDER BY revenue DESC
    LIMIT 1
    """
    return run_query(query)


def top_product():
    query = """
    SELECT product,
           SUM(revenue) AS revenue
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    GROUP BY product
    ORDER BY revenue DESC
    LIMIT 1
    """
    return run_query(query)

def average_order_value():
    query = """
    SELECT
        ROUND(SUM(revenue)/COUNT(order_id),2)
        AS avg_order_value
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    """
    return run_query(query)


def revenue_by_product():
    query = """
    SELECT
        product,
        SUM(revenue) AS total_revenue
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    GROUP BY product
    ORDER BY total_revenue DESC
    """
    return run_query(query)
def total_products():
    query = """
    SELECT COUNT(DISTINCT product) AS total_products
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    """
    return run_query(query)
def top_orders():
    query = """
    SELECT *
    FROM `bigquery-ai-assistant.sales_analytics.sales`
    ORDER BY revenue DESC
    LIMIT 10
    """
    return run_query(query)