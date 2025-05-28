from dataclasses import dataclass
from typing import Set


@dataclass
class BatchProgress:
    """Progress of batch processing."""

    progress: int
    current_records: Set[int]
