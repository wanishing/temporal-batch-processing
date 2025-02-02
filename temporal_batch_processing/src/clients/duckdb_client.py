from typing import Optional
from urllib.parse import urlparse

import duckdb

from temporal_batch_processing.src.models.config import Config

EXPIRATION_IN_SECONDS = 60 * 55


class DuckDBClient:
    _instance: Optional['DuckDBClient'] = None
    _connection: Optional[duckdb.DuckDBPyConnection] = None

    def __new__(cls, connection: duckdb.DuckDBPyConnection):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connection = connection
        return cls._instance

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        if self._connection != connection:
            self._connection = connection

    @classmethod
    def build(cls, config: Config):
        if cls._instance is not None:
            return cls._instance

        conn = cls._create_instance(config)

        return cls(connection=conn)

    @staticmethod
    def _create_instance(config: Config):
        endpoint = urlparse(config.s3_endpoint)
        duck_db_client = duckdb.connect()
        duck_db_client.execute(f"""
            CREATE SECRET (TYPE S3,
            KEY_ID '{config.aws_access_key_id}',
            SECRET '{config.aws_secret_access_key}',
            REGION '{config.aws_region}',
            ENDPOINT '{endpoint.hostname}:{endpoint.port}',
            USE_SSL '{config.aws_verify}',
            URL_STYLE 'path');""")
        return duck_db_client

    def query(self, query: str):
        return self._connection.query(query)

    def execute(self, query: str):
        return self._connection.execute(query)
