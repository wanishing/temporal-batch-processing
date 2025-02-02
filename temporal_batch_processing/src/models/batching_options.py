from dataclasses import dataclass


@dataclass
class BatchingOptions:
    sliding_window_size: int
    partition_size: int
    batch_size: int
