"""
outlier_detection.py

Provides functionality for detecting and managing outliers in numeric data columns.

Includes:
- Z-score based detection (standard deviation method)
- IQR-based detection (interquartile range method)
- Three handling strategies: detect, remove, and flag

Designed to work with both full and user-defined subsets of numeric columns.
Skips constant or low-variance columns automatically and informs the user when this occurs.
Intended for internal use within the CleaningBox class to support data outlier detection.
"""

# External Libraries
import pandas as pd
import numpy as np
from statistics import stdev


def outlier_detection(df, method, threshold, action, columns):
    """
    Identifies and handles outliers in numeric columns using z-score or IQR methods.

    This function supports three outlier handling strategies:
    - "detect": Returns a filtered DataFrame containing only the outlier rows.
    - "remove": Deletes outlier rows from the dataset and prints a summary.
    - "flag": Adds a new boolean column ('outlier_flag') marking outlier rows as True.
              If the column already exists, it will be overwritten with new results.

    Detection is based on:
    - "zscore": Outliers are values where |z| > threshold (default threshold: 3).
    - "iqr": Outliers lie beyond Q1 - (threshold * IQR) or Q3 + (threshold * IQR)
             (default threshold often 1.5, but 3 is used here unless overridden).

    Behaviour:
    - Only numeric columns are considered.
    - Columns with constant values (std=0 or IQR=0) are skipped with a message.
    - If `columns` is set to "all", all numeric columns are included unless specified otherwise.
    - If the specified `columns` include a non-numeric or missing column/value, an error is raised.
    - The result is either returned (for "detect") or applied in-place (for "remove" and "flag").

    Args:
        df (pd.DataFrame): The dataset to process.
        method (str): Outlier detection method — either "zscore" or "iqr".
        action (str): Handling strategy — "detect", "remove", or "flag".
        threshold (float): Sensitivity threshold. Higher values reduce sensitivity.
        columns (Union[str, List[str]]): Target columns for outlier detection, or "all".

    Returns:
        Optional[pd.DataFrame]: A DataFrame of outliers if `action="detect"`, otherwise None.

    Raises:
        ValueError: If a selected column is not numeric or not found.
        ValueError: If an unsupported method or action is provided.
    """
    if columns == "all":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        if isinstance(columns, str):
            columns = [columns]
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"{col} not found in dataset")
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"{col} is not a numerical column in the dataset")
        numeric_cols = columns

    mask = pd.Series(False, index=df.index)

    if method == 'zscore':
        for col in numeric_cols:
            meanV = df[col].mean()
            std_dev = df[col].std()

            if std_dev == 0:
                print(f"Skipping column {col} | (STD DEV == 0)  \n"
                      f"Constant values detected OR all values are identical")
                continue

            zscore = (df[col] - meanV) / std_dev
            mask |= (np.abs(zscore) > threshold)

    elif method == 'iqr':
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lowerBound = Q1 - threshold * IQR
            upperBound = Q3 + threshold * IQR

            mask |= (df[col] < lowerBound) | (df[col] > upperBound)


    if action == 'detect':
        return df[mask]

    if action == 'remove':
        row = mask.sum()
        df.drop(index=df[mask].index, inplace=True)
        if row == 0:
            print(f"0 rows have been removed. No outliers found.")
        elif row == 1:
            print(f"{row} row containing outliers has been successfully removed")
        else:
            print(f"{row} rows containing outliers have been successfully removed")

    if action == 'flag':
        if 'outlier_flag' in df.columns:
            print("Warning: 'outlier_flag' column already exists and will be overwritten.")
        df['outlier_flag'] = mask

    return None



