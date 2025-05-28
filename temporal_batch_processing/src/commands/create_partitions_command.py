from typing import List

from temporal_batch_processing.src.models.file_metadata import FileMetadata
from temporal_batch_processing.src.models.partition_info import PartitionInfo


class CreatePartitionsCommand:
    @staticmethod
    def run(
        files_metadata: List[FileMetadata], partition_size: int
    ) -> List[PartitionInfo]:
        partitions = []

        for file_info in files_metadata:
            remaining_records = file_info.total_records
            current_offset = 0

            while remaining_records > 0:
                current_partition_size = min(remaining_records, partition_size)

                partition = PartitionInfo(
                    file_info=file_info,
                    start_offset=current_offset,
                    end_offset=current_offset + current_partition_size,
                )
                partitions.append(partition)

                current_offset += current_partition_size
                remaining_records -= current_partition_size

        return partitions
