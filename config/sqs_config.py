import boto3
from dotenv import load_dotenv
import os

load_dotenv()

sqs = boto3.client(
    'sqs',
    endpoint_url=os.getenv("SQS_ENDPOINT_URL"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

queue_url = os.getenv("SQS_QUEUE_URL")