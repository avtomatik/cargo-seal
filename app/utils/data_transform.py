import pandas as pd

from app.utils.text import clean_string, transliterate_to_latin


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes the column names by applying a series of transformations:
    1. Trimming whitespaces with a custom trim function.
    2. Transliteration of non-ASCII characters.
    3. Converting the names to lowercase.
    """
    def clean_column_name(col: str) -> str:
        return str.lower(transliterate_to_latin(clean_string(col, fill='_')))

    df.columns = [clean_column_name(col) for col in df.columns]
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
    return df.pipe(standardize_column_names).pipe(drop_empty_rows_and_columns)
