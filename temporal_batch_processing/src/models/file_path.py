from dataclasses import dataclass


@dataclass
class FilePath:
    bucket: str
    key: str

    def to_path(self):
        return f"s3://{self.bucket}/{self.key}"
