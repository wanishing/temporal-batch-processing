import uuid
from typing import List

import duckdb

from temporal_batch_processing.src.clients.duckdb_client import DuckDBClient
from temporal_batch_processing.src.models.config import Config
from temporal_batch_processing.src.models.file_metadata import FileMetadata
from temporal_batch_processing.src.models.file_path import FilePath


class FetchFilesMetadataCommand:
    def __init__(self, duck_db_client: duckdb.DuckDBPyConnection):
        self.duck_db_client = duck_db_client

    @classmethod
    def build(cls, config: Config):
        return cls(duck_db_client=DuckDBClient.build(config))

    def run(
        self, batches_path: FilePath, batches_to_process: List[str]
    ) -> List[FileMetadata]:
        files_metadata: List[FileMetadata] = []
        for batch_id, batch_path in enumerate(batches_to_process):
            parquet_file = FilePath(bucket=batches_path.bucket, key=batch_path)
            parquet_path = parquet_file.to_path()
            total_records = self.duck_db_client.execute(f"""
                SELECT COUNT(*) 
                FROM read_parquet('{parquet_path}')
            """).fetchone()[0]
            random_suffix = str(uuid.uuid4()).replace("-", "")
            table_name = f"batch_{batch_id}_{random_suffix}"
            files_metadata.append(
                FileMetadata(
                    table_name=table_name,
                    file_path=parquet_file,
                    total_records=total_records,
                )
            )
        return files_metadata
