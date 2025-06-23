import pandas as pd

from app.utils.text import regex_trim_country, regex_trim_for_orders


class Validator:
    def run(self, df: pd.DataFrame) -> None:
        for row in ['disport_locality', 'disport_country']:
            df.at[row, 'current'] = regex_trim_for_orders(
                df.at[row, 'current'])

        df.at['disport_locality', 'current'] = regex_trim_country(
            df.at['disport_locality', 'current'])

        loc = df.at['disport_locality', 'current'].strip().lower()
        cty = df.at['disport_country', 'current'].strip().lower()
        if loc == cty:
            df.at['disport_locality', 'current'] = 'Unknown'
