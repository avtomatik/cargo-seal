from pathlib import Path

import pandas as pd

from app.constants import CONFIG_FILE_PATH
from app.services.loaders import ConfigLoader
from app.services.normalizers import Normalizer
from app.services.port_patchers import PortPatcher
from app.services.summary_preprocessor import (IndexAssigner,
                                               SummaryPreprocessor)
from app.services.validators import Validator


class SummaryFromExcelProcessor:
    def __init__(self, config_path: Path = CONFIG_FILE_PATH):
        self.general_config = ConfigLoader(config_path).load()
        self.index_map = {
            int(k): v['columns']
            for k, v in self.general_config.get('columns', {}).items()
        }
        self.default_index = (
            self.general_config.get('default', {}).get('default_index', [])
        )

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
