import re
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook


class ExcelReader:
    def get_details(self, file_path: Path) -> tuple[list[str], str]:
        workbook = load_workbook(file_path, read_only=True, keep_links=False)
        sheet_names = workbook.sheetnames
        operator = workbook.properties.lastModifiedBy
        workbook.close()
        return sheet_names, operator

    def read_sheet(self, file_path: Path, sheet_name: str) -> pd.DataFrame:
        return (
            pd.read_excel(**self._get_kwargs(file_path, sheet_name))
            .dropna(axis=0)
        )

    @staticmethod
    def _get_kwargs(filepath: Path, sheet: str) -> dict:
        base = {'io': filepath, 'sheet_name': sheet}
        special = {
            'declaration_form': {
                'names': ('headers', 'current'),
                'skiprows': 1,
                'index_col': 0,
            }
        }
        return {**base, **special.get(sheet, {})}


def clean_string(
    text: str,
    fill: str = ' ',
    pattern: str = r'\W'
) -> str:
    return fill.join(part for part in re.split(pattern, text.strip()) if part)
