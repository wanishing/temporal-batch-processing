from typing import List

import boto3
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from temporal_batch_processing.src.models.config import Config

    # from temporal_batch_processing.src.models.config import Config, get_config
    from temporal_batch_processing.src.models.file_path import FilePath


class ListFilesCommand:
    def __init__(self, s3_client):
        self.s3_client = s3_client

    @classmethod
    def build(cls, config: Config):
        return cls(
            s3_client=boto3.resource(
                "s3",
                endpoint_url=config.s3_endpoint,
                region_name=config.aws_region,
                aws_access_key_id=config.aws_access_key_id,
                aws_secret_access_key=config.aws_secret_access_key,
                aws_session_token=config.aws_session_token,
                verify=config.aws_verify,
            )
        )

    def list_files(self, file_path: FilePath) -> List[str]:
        key = file_path.key if file_path.key.endswith("/") else f"{file_path.key}/"
        bucket = self.s3_client.Bucket(file_path.bucket)
        objects = bucket.objects.filter(Prefix=key)
        return [obj.key for obj in objects if obj.key.endswith(".parquet")]


# config = get_config()
# cmd = ListFilesCommand.build(config)
# print(config)
# print(cmd.list_files(FilePath(bucket='some-bucket', key='some-key')))
