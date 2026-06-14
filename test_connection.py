from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "credentials/service-account.json"
)

client = bigquery.Client(
    project="bigquery-ai-assistant"
)

print("Connected Successfully!")

datasets = list(client.list_datasets())

for dataset in datasets:
    print(dataset.dataset_id)