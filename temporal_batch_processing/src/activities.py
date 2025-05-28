from typing import List

from temporalio import activity

from temporal_batch_processing.src.commands.create_partitions_command import (
    CreatePartitionsCommand,
)
from temporal_batch_processing.src.commands.enrich_order_command import (
    EnrichOrdersCommand,
)
from temporal_batch_processing.src.commands.fetch_files_metadata_command import (
    FetchFilesMetadataCommand,
)
from temporal_batch_processing.src.commands.list_files_command import ListFilesCommand
from temporal_batch_processing.src.commands.read_orders_command import ReadOrdersCommand
from temporal_batch_processing.src.generated_protos.order_pb2 import EnrichOrderRequests
from temporal_batch_processing.src.models.config import get_config
from temporal_batch_processing.src.models.file_metadata import FileMetadata
from temporal_batch_processing.src.models.file_path import FilePath
from temporal_batch_processing.src.models.partition_info import PartitionInfo


@activity.defn
async def list_files_activity(file_path: FilePath) -> List[str]:
    return ListFilesCommand.build(get_config()).list_files(file_path)


@activity.defn
async def fetch_files_metadata_activity(
    batches_path: FilePath, batches_to_process: List[str]
) -> List[FileMetadata]:
    return FetchFilesMetadataCommand.build(get_config()).run(
        batches_path, batches_to_process
    )


@activity.defn
async def create_partitions_activity(
    files_metadata: List[FileMetadata], partition_size: int
) -> List[PartitionInfo]:
    return CreatePartitionsCommand.run(files_metadata, partition_size)


@activity.defn
async def cleanup_temporary_table_activity(table_name: str) -> None:
    CleanTableCommand.build(get_config()).run(table_name)


@activity.defn
async def read_orders_activity(
    file_info: FileMetadata, start_offset: int, limit: int
) -> EnrichOrderRequests:
    return ReadOrdersCommand.build(get_config()).run(file_info, start_offset, limit)


@activity.defn
async def enrich_orders_activity(orders: EnrichOrderRequests) -> None:
    return EnrichOrdersCommand.build(get_config()).run(orders)
