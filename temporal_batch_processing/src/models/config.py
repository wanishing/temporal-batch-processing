import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    temporal_server: str
    task_queue: str
    s3_endpoint: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: Optional[str]
    aws_verify: bool
    order_service_host: str
    order_service_port: str


def get_config():
    return Config(
        temporal_server=os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
        task_queue=os.environ.get("TASK_QUEUE", "batch-processing-task-queue"),
        s3_endpoint=os.environ.get("S3_ENDPOINT", "http://127.0.0.1:5050"),
        aws_region=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN", None),
        aws_verify=os.environ.get("AWS_VERIFY", "false").lower() == "true",
        order_service_host=os.environ.get("ORDER_SERVICE_HOST", "localhost"),
        order_service_port=os.environ.get("ORDER_SERVICE_PORT", "7070")
    )
