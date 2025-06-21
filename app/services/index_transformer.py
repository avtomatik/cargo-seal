class IndexMapTransformer:
    @staticmethod
    def transform(raw_data: dict[str, list[str]]) -> dict[int, list[str]]:
        return {int(k): v for k, v in raw_data.items()}
