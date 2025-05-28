from dataclasses import dataclass

from temporal_batch_processing.src.models.batching_options import BatchingOptions
from temporal_batch_processing.src.models.file_path import FilePath


@dataclass
class BatchProcessingRequest:
    files_path: FilePath
    batching_options: BatchingOptions
