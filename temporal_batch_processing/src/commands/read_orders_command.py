from typing import List

from temporal_batch_processing.src.clients.duckdb_client import DuckDBClient
from temporal_batch_processing.src.generated_protos.order_pb2 import EnrichOrderRequests, EnrichOrderRequest
from temporal_batch_processing.src.models.config import Config
from temporal_batch_processing.src.models.file_metadata import FileMetadata
from temporal_batch_processing.src.models.file_path import FilePath


class ReadOrdersCommand:

    def __init__(self, duckdb_client: DuckDBClient):
        self.duck_db_client = duckdb_client

    @classmethod
    def build(cls, config: Config):
        return cls(duckdb_client=DuckDBClient.build(config))

    def run(self, file_info: FileMetadata,
            start_offset: int,
            limit: int) -> EnrichOrderRequests:
        self._create_view_if_not_exist(file_info.file_path, file_info.table_name)
        orders_table = self.read_orders_by(file_info, start_offset, limit)
        raw_orders = orders_table.fetchall()
        orders = self._to_protobuf(raw_orders)
        return EnrichOrderRequests(requests=orders)

    def read_orders_by(self, file_info: FileMetadata,
                       start_offset: int,
                       limit: int):
        columns_to_select: List[str] = ['order_id', 'email', 'created_at']
        select_stmt: str = f"SELECT {','.join(columns_to_select)} FROM {file_info.table_name} LIMIT {limit} OFFSET {start_offset}"
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

    def _create_view_if_not_exist(self, parquet_path: FilePath, view_name: str):

        """
        Creates a view from a parquet file if it doesn't already exist.

        Args:
            parquet_path: Path to the parquet file
            view_name: Name for the view to be created
        """

        check_view_query = f"""
            SELECT COUNT(*) 
            FROM duckdb_views() 
            WHERE view_name = '{view_name.lower()}'
        """

        view_exists = self.duck_db_client.execute(check_view_query).fetchone()[0] > 0

        if not view_exists:
            create_view_query = f"""
            CREATE VIEW {view_name} AS 
            SELECT * FROM read_parquet('{parquet_path.to_path()}')
            """
            self.duck_db_client.execute(create_view_query)
