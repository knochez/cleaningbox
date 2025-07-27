"""
binarization.py

Provides a function to convert categorical values into binary (0/1) form.

- `binarization_func(df, columns, positive_value, negative_value)`:
  Transforms values in the specified columns into binary based on user-defined
  or default mappings ("yes" → 1, "no" → 0).

Used internally by the CleaningBox class to simplify binary classification
or feature engineering for machine learning pipelines.
"""

# External Libraries
import pandas as pd
import numpy as np


def binarization_func(df, columns, positive_value, negative_value):
    """
    Converts categorical values in specified columns to binary (0/1) format.

    This function supports two modes of operation:
    - Default mode: If both `positive_value` and `negative_value` are None,
      the function maps "yes" → 1 and "no" → 0.
    - Custom mode: The user must provide both `positive_value` and `negative_value`
      as lists of values to be mapped to 1 and 0, respectively.

    All values in each specified column must match one of the provided mappings.
    An error is raised if any unmapped values are found.

    Args:
        df (pd.DataFrame): The dataset containing the columns to transform.
        columns (List[str]): List of column names to apply binarization to.
        positive_value (Optional[List[str]]): Values to be mapped to 1.
        negative_value (Optional[List[str]]): Values to be mapped to 0.

    Raises:
        ValueError: If only one of `positive_value` or `negative_value` is provided.
        ValueError: If a column contains values not found in the mapping.
    """
    if positive_value is None and negative_value is None:
        binary_map = {
            "yes": 1,
            "no": 0
        }
    elif positive_value and negative_value:
        binary_map = {val: 1 for val in positive_value} | {val: 0 for val in negative_value}
    else:
        raise ValueError("Both positive_value and negative_value must be provided or both must be None.")

    for col in columns:
        df[col] = df[col].astype(str)

        unique_vals = set(df[col].unique())
        unknowns = unique_vals - set(binary_map.keys())

        if unknowns:
            raise ValueError(f"Column '{col}' contains unmapped values: {unknowns}")

        df[col] = df[col].map(binary_map).astype(int)




