from dataclasses import dataclass


@dataclass
class PartitionWorkflowProgress:
    child_id: str
    completed: int
