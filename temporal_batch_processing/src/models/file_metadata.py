from dataclasses import dataclass

from temporal_batch_processing.src.models.file_path import FilePath


@dataclass
class FileMetadata:
    total_records: int
    file_path: FilePath
