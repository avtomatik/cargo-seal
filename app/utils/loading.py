from pathlib import Path

from app.services.file_loader import JsonFileLoader
from app.services.index_transformer import IndexMapTransformer


def load_index_map(path: Path) -> dict[int, list[str]]:
    loader = JsonFileLoader.from_path(path)
    raw_data = loader.load()
    return IndexMapTransformer.transform(raw_data)
