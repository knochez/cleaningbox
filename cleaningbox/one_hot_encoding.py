"""
one_hot_encoding.py

Provides functionality for applying one-hot encoding to categorical columns.

Replaces specified categorical columns with new binary indicator columns representing each category.
Supports optional removal of the first category to avoid multicollinearity in models.

Used internally by the CleaningBox class for preparing categorical data for machine learning workflows.
"""

# External Libraries
import pandas as pd
import numpy as np


def one_hot_encoding_func(df, columns, drop_first):
    """
    Applies one-hot encoding to specified categorical columns in the dataset.

    Converts each unique category in a column into a separate binary (0/1) column.
    The original categorical column is removed after encoding. By default, the first
    category in each column is dropped to prevent the dummy variable trap.

    Args:
        df (pd.DataFrame): The input dataset.
        columns (Union[str, List[str]]): Column name or list of categorical columns to encode.
        drop_first (bool): If True, drops the first category in each encoded column. Defaults to True.

    Raises:
        ValueError: If a specified column is not found in the dataset.
        ValueError: If a specified column is not of categorical dtype.
    """
    if isinstance(columns, str):
        columns = [columns]
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"{col} not found in dataset")
        if pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(
                f"{col} appears to be numeric — one-hot encoding is usually intended for categorical columns.")

    cat_cols = columns

    OHE_df = pd.get_dummies(df[cat_cols], drop_first=drop_first).astype(int)
    df.drop(columns=cat_cols, inplace=True)
    df[OHE_df.columns] = OHE_df


