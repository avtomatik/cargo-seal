import json
from pathlib import Path
from typing import List, Union


class JsonFileLoader:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> Union[List[dict], dict[str, str]]:
        with self.file_path.open(encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def from_path(cls, path: Path):
        return cls(path)
