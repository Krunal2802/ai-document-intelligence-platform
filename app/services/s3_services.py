import boto3
from app.core.config import settings
import uuid
from fastapi import UploadFile

class S3Service:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def generate_s3_key(
        self,
        user_id: int,
        knowledge_base_id: int,
        filename: str
    ):
        unique_filename = f"{uuid.uuid4()}_{filename}"

        return (
            f"users/{user_id}/"
            f"knowledge_bases/{knowledge_base_id}/"
            f"documents/{unique_filename}"
        )

    def upload_file_to_s3(
        self,
        file: UploadFile, 
        s3_key:  str
    ):
        self.client.upload_fileobj(
            Fileobj = file.file,
            Bucket = settings.AWS_S3_BUCKET,
            Key = s3_key
        )
        return s3_key

    def delete_file_from_s3(
        self,
        s3_key: str 
    ):
        self.client.delete_object(
            Bucket=settings.AWS_S3_BUCKET,
            Key=s3_key
        )

    def list_buckets(self):
        response = self.client.list_buckets()

        return [bucket["Name"] for bucket in response["Buckets"]]