from src.bigquery_helper import run_query

query = """
SELECT COUNT(*) AS total_rows
FROM `bigquery-ai-assistant.sales_analytics.sales`
"""

results = run_query(query)

print(results)