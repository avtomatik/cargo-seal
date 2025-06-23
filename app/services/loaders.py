from pathlib import Path


class ConfigLoader:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict:
        import yaml
        with self.path.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f)
