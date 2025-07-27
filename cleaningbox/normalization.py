"""
normalization.py

Provides normalization functions for numeric columns in tabular datasets.

Includes support for:
- Min-Max scaling (0 to 1 range)
- Z-score standardization (mean-centered, std-scaled)
- Robust scaling (median-centered, IQR-scaled)

The module handles edge cases such as constant columns or low variance
by skipping normalization and issuing informative messages.

Used internally by the CleaningBox class to standardize datasets before
analysis or modeling.
"""

# External Libraries
import pandas as pd
import numpy as np
from statistics import stdev


def normalization_func(df, method, columns, exclude):
    """
    Applies normalization to all, or a specified set of, numeric columns in the dataset.

    Supports three normalization strategies:
    - "minmax": Scales values to the [0, 1] range based on min/max.
    - "zscore": Standardizes values by subtracting the mean and dividing by the standard deviation.
    - "robust": Centers values around the median and scales by the interquartile range (IQR).

    Behaviour:
    - If `columns` is set to "all", all numeric columns are considered unless excluded.
    - If `exclude` is provided, listed columns are skipped even when "all" is selected.
    - Columns with constant values (e.g., identical min/max, std dev = 0, or IQR = 0) are skipped with a printed message.
    - Non-numeric columns are ignored unless explicitly selected, in which case an error is raised.

    Args:
        df (pd.DataFrame): The input dataset.
        method (str): The normalization method — "minmax", "zscore", or "robust".
        columns (Union[str, List[str]]): Columns to normalize. Can be a single name, list of names, or "all" (by default).
        exclude (Union[str, List[str], None]): Optional column(s) to exclude from normalization.

    Raises:
        ValueError: If a specified column does not exist or is not numeric.
        ValueError: If `method` is not one of the supported options.
    """
    if columns != "all" and isinstance(columns, str):
        columns = [columns]
    if exclude and isinstance(exclude, str):
        exclude = [exclude]

    if columns == "all":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if exclude:
            numeric_cols = numeric_cols.drop(exclude)
    else:
        if isinstance(columns, str):
            columns = [columns]
        for column in columns:
            if column not in df.columns:
                raise ValueError(f"{column} not found in the dataset")
            elif not pd.api.types.is_numeric_dtype(df[column]):
                raise ValueError(f"{column} is not a numerical column in the dataset")
        numeric_cols = columns

    if method == "minmax":
        for col in numeric_cols:
            minV = df[col].min()
            maxV = df[col].max()

            if maxV == minV:
                print(f"Skipping column {col} | (maxV == minV) \n"
                      f"Constant values detected")
            else:
                df[col] = (df[col] - minV) / (maxV - minV)


    if method == "zscore":
        for col in numeric_cols:
            meanV = df[col].mean()
            std_dev = df[col].std()

            if std_dev == 0:
                print(f"Skipping column {col} | (STD DEV == 0)  \n"
                      f"Constant values detected OR all values are identical")
            else:
                df[col] = (df[col] - meanV) / std_dev


    if method == "robust":
        for col in numeric_cols:
            medianV = df[col].median()
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            if IQR == 0:
                print(f"Skipping Column {col} | (IQR == 0) \n"
                      f"Constant or low variance")
            else:
                df[col] = (df[col] - medianV) / IQR


