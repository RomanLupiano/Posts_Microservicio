from google.cloud import storage
import os
from dotenv import load_dotenv

load_dotenv()

credentials = os.getenv("CREDENTIALS_FILE")
bucket_name = os.getenv("BUCKET_NAME")
print(credentials)
print(bucket_name)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)