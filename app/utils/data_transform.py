import pandas as pd

from app.utils.text import RegexStringCleaner, transliterate_to_latin


class ColumnTransformer:
    def __init__(
        self,
        cleaner: RegexStringCleaner,
        transliterate_func,
        lower: bool = True
    ):
        self.cleaner = cleaner
        self.transliterate = transliterate_func
        self.lower = lower

    def transform(self, name: str) -> str:
        result = self.cleaner.clean(name)
        result = self.transliterate(result)
        return result.lower() if self.lower else result


def standardize_column_names(
    df: pd.DataFrame,
    transformer: ColumnTransformer
) -> pd.DataFrame:
    df.columns = [transformer.transform(col) for col in df.columns]
    return df


def drop_empty_rows_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops rows and columns that are completely empty.
    """
    return df.dropna(axis=0, how='all').dropna(axis=1, how='all')


def standardize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes the dataset by cleaning column names and dropping empty rows and columns.
    """
    cleaner = RegexStringCleaner(fill='_')
    transformer = ColumnTransformer(cleaner, transliterate_to_latin)
    return (
        df
        .pipe(standardize_column_names, transformer)
        .pipe(drop_empty_rows_and_columns)
    )
