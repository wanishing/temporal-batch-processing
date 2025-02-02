from dataclasses import dataclass, field
from typing import Set

from temporal_batch_processing.src.models.file_metadata import FileMetadata


@dataclass
class PartitionWorkflowInput:
    file_info: FileMetadata
    end_offset: int
    sliding_window_size: int
    batch_size: int
    start_offset: int = 0
    progress: int = 0
    in_process_records: Set[int] = field(default_factory=set)
