from typing import List

from temporal_batch_processing.src.clients.duckdb_client import DuckDBClient
from temporal_batch_processing.src.generated_protos.order_pb2 import (
    EnrichOrderRequests,
    EnrichOrderRequest,
)
from temporal_batch_processing.src.models.config import Config
from temporal_batch_processing.src.models.file_metadata import FileMetadata


class ReadOrdersCommand:
    def __init__(self, duckdb_client: DuckDBClient):
        self.duck_db_client = duckdb_client

    @classmethod
    def build(cls, config: Config):
        return cls(duckdb_client=DuckDBClient.build(config))

    def run(
        self, file_info: FileMetadata, start_offset: int, limit: int
    ) -> EnrichOrderRequests:
        orders_table = self.read_orders_by(file_info, start_offset, limit)
        raw_orders = orders_table.fetchall()
        orders = self._to_protobuf(raw_orders)
        return EnrichOrderRequests(requests=orders)

    def read_orders_by(self, file_info: FileMetadata, start_offset: int, limit: int):
        columns_to_select: List[str] = ["order_id", "email", "created_at"]
        select_stmt: str = f"SELECT {','.join(columns_to_select)} FROM read_parquet('{file_info.file_path.to_path()}') LIMIT {limit} OFFSET {start_offset}"
        orders_table = self.duck_db_client.query(select_stmt)
        return orders_table

    @staticmethod
    def _to_protobuf(raw_orders):
        orders_as_protobuf = []
        for raw_orders in raw_orders:
            obj = EnrichOrderRequest()
            obj.order_id = str(raw_orders[0])
            obj.email = str(raw_orders[1])
            obj.created_at = str(raw_orders[2])
            orders_as_protobuf.append(obj)
        return orders_as_protobuf
