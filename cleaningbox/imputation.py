"""
imputation.py

Provides functions for handling missing data in tabular datasets.

- `impute_missing(df)`: Fills missing values using statistical strategies
  appropriate for numeric (mean/median) and categorical (mode) columns.
- `missing_values(df, verbose)`: Analyzes and reports missing data patterns,
  with customizable verbosity levels for summaries or automation.

Used internally by the CleaningBox class to identify and treat missing values
as part of a structured data cleaning pipeline.
"""


# External Libraries
import pandas as pd
import numpy as np


def impute_missing(df):
    """
    Performs missing value imputation on both numeric and categorical columns.

    For numeric columns:
    - Uses median if the column's skewness is high (|skew| > 1), otherwise uses mean.
    - Columns containing only missing values are skipped and reported.

    For categorical columns:
    - Uses the most frequent value (mode) to fill missing entries.
    - Columns with only missing values are also skipped and reported.

    Columns skipped due to having no valid data are listed for transparency.

    Args:
        df (pd.DataFrame): The dataset with missing values to impute.

    Returns:
        pd.DataFrame: The DataFrame with missing values filled.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    num_fill = {}
    skipped_numeric = []

    for col in numeric_cols:
        if df[col].isna().all():
            skipped_numeric.append(col)
            continue
        fill_value = df[col].median() if abs(df[col].skew()) > 1 else df[col].mean()
        if pd.notna(fill_value):
            num_fill[col] = fill_value

    df[numeric_cols] = df[numeric_cols].fillna(num_fill)

    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    cat_fill = {}
    skipped_cat = []

    for col in cat_cols:
        if df[col].isna().all():
            skipped_cat.append(col)
            continue
        mode = df[col].mode()
        if not mode.empty:
            cat_fill[col] = mode[0]

    df[cat_cols] = df[cat_cols].fillna(cat_fill).astype("category")

    if skipped_numeric or skipped_cat:
        print("⚠️ Imputation skipped for columns with all values missing:")
        if skipped_numeric:
            print(f"  -  Skipped columns: {', '.join(skipped_numeric)}")
        if skipped_cat:
            print(f"  - Skipped columns: {', '.join(skipped_cat)}")

    return df


def missing_values(df, verbose: str = "false"):
    """
    Checks for missing values in the dataset and provides reporting or logical feedback.

    This function scans the DataFrame for NaN (missing) values and behaves according to the
    verbosity level specified:

    - "false": Prints a brief summary, including total missing values, affected columns,
               total cell count, and percentage of missing data.
    - "true": Prints the same summary as "false", plus a detailed table listing each
              column with missing values, how many are missing, and the percentage.
    - "silent": Suppresses all output and returns a Boolean indicating whether any
                missing values were found (True if any missing, False otherwise).

    If no missing values are found:
    - "false" and "true": Print "✓ Dataset is clean".
    - "silent": Returns False.

    If missing values are found and "true" is selected:
    - A table is printed showing:
        - Column name
        - Count of missing values
        - Percentage of missing values

    Args:
        df (pd.DataFrame): The dataset to analyze.
        verbose (str): Mode of reporting — one of "true", "false", or "silent" (case-insensitive).

    Returns:
        Optional[bool]: Returns True/False if verbose is "silent", otherwise returns None.

    Raises:
        ValueError: If an invalid `verbose` option is provided.
    """
    verbose = verbose.lower()

    if verbose not in {"true", "false", "silent"}:
        raise ValueError("Invalid verbose value. Use 'true', 'false', or 'silent'.")

    missVals = df.isna().sum().sum()
    affCols = (df.isna().sum() > 0).sum()

    if missVals == 0:
        if verbose == "silent":
            return False
        print("✓ Dataset is clean")
        return None

    if verbose == "silent":
        return True

    total_cells = df.shape[0] * df.shape[1]
    total_percentage = round((missVals / total_cells) * 100, 2)

    print(f"\n⚠️ Missing values detected\n"
          f"Missing values found: {missVals} | Affected columns: {affCols}\n"
          f"Valid/Missing values: {total_cells} / {missVals} ({total_percentage}%)\n")

    if verbose == "true":
        missing = df.isna().sum()
        missing_df = (
            pd.DataFrame({
                "Missing_Value_Count": missing,
                "Missing_Value_Percentage": (missing / len(df) * 100).round(2)
            })
            .query("Missing_Value_Count > 0")
            .sort_values("Missing_Value_Percentage", ascending=False)
            .reset_index()
            .rename(columns={"index": "Attribute_Name"})
        )
        print(missing_df)

    return None

