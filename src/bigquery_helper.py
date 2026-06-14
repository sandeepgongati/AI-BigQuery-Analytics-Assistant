from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "credentials/service-account.json"
)

client = bigquery.Client(
    project="bigquery-ai-assistant"
)

def run_query(query):
    query_job = client.query(query)
    results = query_job.result()

    rows = []

    for row in results:
        rows.append(dict(row))

    return rows