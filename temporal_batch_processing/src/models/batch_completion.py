from dataclasses import dataclass


@dataclass
class BatchCompletion:
    start: int
    limit: int
