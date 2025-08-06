from pathlib import Path

import toml


class ConfigLoader:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict:
        return toml.load(self.path)
