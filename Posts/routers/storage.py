from google.cloud import storage

storage_client = storage.Client()
bucket_name = "your_bucket_name"
bucket = storage_client.bucket(bucket_name)