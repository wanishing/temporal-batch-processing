from dataclasses import dataclass

from temporal_batch_processing.src.models.file_metadata import FileMetadata


@dataclass
class PartitionInfo:
    file_info: FileMetadata
    start_offset: int
    end_offset: int
