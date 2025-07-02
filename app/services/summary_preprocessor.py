from typing import List, Protocol

import pandas as pd


class DataProcessor(Protocol):
    def run(self, df: pd.DataFrame) -> None:
        ...


class IndexAssigner:
    def __init__(
        self,
        index_map: dict[int, list[str]],
        default_index: list[str]
    ):
        self.index_map = index_map
        self.default_index = default_index

    def run(self, df: pd.DataFrame) -> None:
        df.index = self.index_map.get(df.shape[0], self.default_index)


class SummaryPreprocessor:
    def __init__(
        self,
        df: pd.DataFrame,
        processors: List[DataProcessor],
        index_assigner: IndexAssigner
    ):
        self.df = df.copy()
        self.processors = processors
        self.index_assigner = index_assigner

    def process(self) -> pd.DataFrame:
        self.index_assigner.run(self.df)
        for processor in self.processors:
            processor.run(self.df)
        return self.df
