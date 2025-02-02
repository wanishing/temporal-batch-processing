import uuid
from concurrent import futures
from pathlib import Path

import boto3
import grpc
import pytest
from temporalio.client import Client
from temporalio.testing import WorkflowEnvironment

from temporal_batch_processing.src.generated_protos.order_pb2_grpc import add_OrderServiceServicer_to_server
from temporal_batch_processing.src.models.batch_processing_request import BatchProcessingRequest
from temporal_batch_processing.src.models.batching_options import BatchingOptions
from temporal_batch_processing.src.models.file_path import FilePath
from temporal_batch_processing.src.workflows import MainWorkflow
from temporal_batch_processing.tests.fake_order_service import FakeOrderService

TASK_QUEUE = 'batch-processing-task-queue'
TEMPORAL_SERVER = "localhost:7233"
S3_ENDPOINT = "http://127.0.0.1:5050"
REQUEST = BatchProcessingRequest(
    files_path=FilePath(bucket='some-bucket',
                        key='some-key'),
    batching_options=BatchingOptions(sliding_window_size=4,
                                     partition_size=5,
                                     batch_size=2)
)

EXPECTED_ORDERS_COUNT = 20


@pytest.fixture
def fake_order_service():
    service = FakeOrderService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_OrderServiceServicer_to_server(service, server)
    port = 7070
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    yield service
    server.stop(grace=None)


@pytest.fixture
def fake_s3():
    s3 = boto3.resource("s3",
                        region_name="us-east-1",
                        endpoint_url=S3_ENDPOINT,
                        aws_access_key_id="test",
                        aws_secret_access_key="test",
                        aws_session_token=None)
    yield s3


def _given_files_uploaded(s3, path):
    bucket = s3.create_bucket(Bucket=path.bucket)
    resources_dir = Path('resources').resolve()
    for parquet_file in resources_dir.glob('*.parquet'):
        s3_key = f"{path.key}/{parquet_file.name}"
        bucket.upload_file(
            str(parquet_file),
            s3_key
        )


@pytest.mark.asyncio
async def test_should_process_all_records(fake_s3, fake_order_service):
    _given_files_uploaded(fake_s3, REQUEST.files_path)
    client = await Client.connect(TEMPORAL_SERVER)
    async with WorkflowEnvironment.from_client(client) as env:
        await env.client.execute_workflow(
            MainWorkflow.run,
            args=[REQUEST],
            id=str(uuid.uuid4()),
            task_queue=TASK_QUEUE,
        )

        fake_order_service.assert_requested(EXPECTED_ORDERS_COUNT)
