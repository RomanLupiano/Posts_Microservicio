from fastapi import UploadFile
from google.cloud import storage
import os
from dotenv import load_dotenv

load_dotenv()

credentials = os.getenv("CREDENTIALS_FILE")
bucket_name = os.getenv("BUCKET_NAME")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

def upload_image(image: UploadFile) -> str:
    blob = bucket.blob(image.filename)
    blob.upload_from_file(image.file, content_type=image.content_type)
    return blob.public_url