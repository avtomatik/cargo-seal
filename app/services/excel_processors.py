from pathlib import Path

import pandas as pd

from app.constants import COL_FILE_PATH, GEN_FILE_PATH
from app.services.loaders import ConfigLoader
from app.services.normalizers import Normalizer
from app.services.port_patchers import PortPatcher
from app.services.summary_preprocessor import (IndexAssigner,
                                               SummaryPreprocessor)
from app.services.validators import Validator


class SummaryFromExcelProcessor:
    def __init__(
        self,
        config_path: Path = GEN_FILE_PATH,
        column_path: Path = COL_FILE_PATH
    ):
        self.general_config = ConfigLoader(config_path).load()
        self.index_map = ConfigLoader(column_path).load()
        self.default_index = self.general_config.get('default_index', [])

    def process(self, df_summary_raw: pd.DataFrame) -> pd.DataFrame:
        processors = [
            Normalizer(config=self.general_config),
            Validator(),
            PortPatcher(config=self.general_config),
        ]

        preprocessor = SummaryPreprocessor(
            df=df_summary_raw,
            processors=processors,
            index_assigner=IndexAssigner(self.index_map, self.default_index),
        )

        return preprocessor.process()
