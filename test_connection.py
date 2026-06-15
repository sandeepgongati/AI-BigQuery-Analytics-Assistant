from google.cloud import bigquery


client = bigquery.Client(
    project="bigquery-ai-assistant"
)

print("Connected Successfully!")

datasets = list(client.list_datasets())

for dataset in datasets:
    print(dataset.dataset_id)