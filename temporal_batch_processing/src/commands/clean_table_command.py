from temporal_batch_processing.src.clients.duckdb_client import DuckDBClient


class CleanTableCommand:

    def __init__(self, duckdb_client: DuckDBClient):
        self.duck_db_client = duckdb_client

    @classmethod
    def build(cls, config):
        return cls(duckdb_client=DuckDBClient.build(config))

    def run(self, table_name: str) -> None:
        query = f"""
        DROP VIEW IF EXISTS {table_name};
        """
        self.duck_db_client.execute(query)
