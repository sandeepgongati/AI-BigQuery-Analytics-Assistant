from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "credentials/service-account.json"
)

client = bigquery.Client(
    project="bigquery-ai-assistant"
)

table_id = (
    "bigquery-ai-assistant.sales_analytics.sales"
)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
)

with open("data/retail_sales.csv", "rb") as source_file:
    load_job = client.load_table_from_file(
        source_file,
        table_id,
        job_config=job_config,
    )

load_job.result()

print("500 records loaded successfully!")