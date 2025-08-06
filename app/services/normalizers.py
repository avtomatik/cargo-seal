import pandas as pd

from app.utils.text import clean_string, regex_trim_entity


class Normalizer:
    def __init__(self, config: dict):
        self.rows_to_clean = config.get('default', {}).get('rows_to_clean', [])
        self.entity_trim_rows = config.get('default', {}).get(
            'entity_trim_rows',
            ['insured', 'counterparty']
        )

    def run(self, df: pd.DataFrame) -> None:
        for row in self.rows_to_clean:
            df.at[row, 'current'] = clean_string(
                df.at[row, 'current'], ' ').title()

        for row in self.entity_trim_rows:
            df.at[row, 'current'] = regex_trim_entity(df.at[row, 'current'])
