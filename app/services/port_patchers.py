import pandas as pd


class PortPatcher:
    def __init__(self, config):
        self.to_replace = config.get('port_replacements', {})
        self.to_remove = config.get('values_to_remove', [])

    def run(self, df: pd.DataFrame):
        df['current'] = df['current'].replace(self.to_remove, 'Unknown')
        df['current'] = df['current'].replace(self.to_replace)
