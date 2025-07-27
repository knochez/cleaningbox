""""
core.py

Defines the CleaningBox class, which serves as the main interface for
loading, transforming, and exporting tabular datasets. It executes
all cleaning operations such as imputation, encoding, binarization, and outlier handling.
"""

# External Libraries
import pandas as pd
import numpy as np
import os
from typing import Union, Optional, List, Any

# Local Files
from .imputation import impute_missing, missing_values
from .binarization import binarization_func
from .normalization import normalization_func
from .one_hot_encoding import one_hot_encoding_func
from .outlier_detection import outlier_detection


class cleaningbox:
    def __init__(self) -> None:
        """
        Initializes an empty CleaningBox instance.

        Sets up the internal DataFrame container, which will hold the active dataset
        once loaded via the `load_data()` method. All cleaning operations refer to this container.
        """
        self.df = None


    def load_data(self, dataset: str, missingvalues: Optional[List[Any]] = None) -> None:
        """
        Loads a dataset from a file into the internal DataFrame.

        Supported Excel extensions: .csv, .xlsx, .xls, and .ods. The appropriate reader function is selected based on
        the file extension. By default, empty cells/entries are treated as missing values. Optionally, the user may
        specify custom values that should also be interpreted as missing. These are internally converted to NaN.

        Args: dataset: Path to the dataset file. Must be a supported format. missingvalues: Optional list of values (
        e.g., strings like 'Unknown', or numbers like 0) to treat as missing.

        Raises:
            ValueError: If the file extension is not supported.
        """

        if missingvalues is None:
            missingvalues = []

        file_extension = os.path.splitext(dataset.lower())[1]
        file_readers = {
            '.csv': pd.read_csv,
            '.xlsx': pd.read_excel,
            '.xls': pd.read_excel,
            '.ods': pd.read_excel
        }

        reader = file_readers.get(file_extension)
        if reader:
            self.df = reader(
                dataset,
                na_values=missingvalues,
                keep_default_na=True
            )
        else:
            raise ValueError(f"Unsupported file type: {file_extension} in {dataset}")


    def get_data(self) -> pd.DataFrame:
        """
        Returns a copy of the currently loaded dataset.

        This method allows users to retrieve the internal DataFrame as a standalone variable. Once assigned,
        the dataset behaves like any standard Pandas DataFrame and can be used in external workflows, libraries,
        or custom analyses.

        Examples:
            df = cb.get_data()
            df.head(10)

            # Chaining usage without assignment
            print(cb.get_data().columns.tolist())

            import seaborn as sns
            sns.boxplot(data=cb.get_data(), x="job", y="salary")

        Returns:
            pd.DataFrame: The currently loaded dataset.

        Raises:
            ValueError: If no dataset has been loaded.
        """
        if self.df is None:
            raise ValueError("No dataset loaded.")
        return self.df


    def export_data(self, setFilename: str, fileIndex: bool = False) -> None:
        """
        Exports the current dataset to a file in the specified format.

        Supports saving to .csv, .xlsx, .xls, and .ods formats. The export method is
        automatically chosen based on the file extension provided. The user can also
        control whether to include the index column during export.

        Args:
            setFilename: Name of the output file, including the desired extension.
            fileIndex: Whether to include the DataFrame's index in the output file. Defaults to False.

        Raises:
            ValueError: If no dataset is loaded, or if the file extension is unsupported.
        """
        if self.df is None:
            raise ValueError(f"Dataset file not found")
        else:
            fileExtensionGetter = os.path.splitext(setFilename.lower())[1]
            exporters = {
                '.csv': self.df.to_csv,
                '.xlsx': self.df.to_excel,
                '.xls': self.df.to_excel,
                '.ods': self.df.to_excel
            }

            fileReader = exporters.get(fileExtensionGetter)

            if fileReader:
                fileReader(setFilename, index=fileIndex)
            else:
                raise ValueError(f"Unsupported file extension: {fileExtensionGetter}. Supported types are .csv, "
                                 f".xlsx, .xls, .ods")


    def imputation(self) -> None:
        """
        Performs missing value imputation on the current dataset.

        Applies statistical imputation to fill in missing values in the DataFrame.
        The exact strategy is handled internally. This method updates the dataset
        in-place.

        Raises:
            ValueError: If no dataset has been loaded.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        self.df = impute_missing(self.df)


    def find_missing_values(self, verbose: str = "false") -> Optional[bool]:
        """
        Analyzes the current dataset for missing values and optionally reports the results.

        This method checks for NaN values in the dataset and behaves differently based on the
        `verbose` parameter:

        - "false": Prints a short summary (count and percentage of missing values and affected columns).
        - "true": Prints the summary plus a detailed table of missing value counts by column.
        - "silent": Returns a Boolean indicating whether any missing values were found, with no printed output.

        Args:
            verbose: One of "false", "true", or "silent" (case-insensitive).
                Controls the verbosity and output behavior of the method.

        Returns:
            bool or None: Returns True or False when `verbose` is "silent", otherwise None.

        Raises:
            ValueError: If no dataset is loaded, or if an invalid `verbose` option is provided.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        return missing_values(self.df, verbose)


    def viewer(self) -> None:
        """
        Prints the entire dataset currently loaded in the CleaningBox instance.

        This is a convenience method that displays the full DataFrame in the console,
        similar to evaluating a variable directly in a notebook environment. It provides
        a quick overview of the dataset without requiring export or additional setup.

        Raises:
            ValueError: If no dataset is loaded.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        print(self.df)


    def binarization(self, columns: Union[str, List[str]], positive_value: Optional[List[str]] = None,
                     negative_value: Optional[List[str]] = None) -> None:
        """
        Converts categorical values in specified columns into binary form (0/1).

        By default, this method maps the string "yes" to 1 and "no" to 0. The user
        can override this by specifying custom lists of values to be treated as
        positive (1) and negative (0). All other values will trigger an error unless
        explicitly handled.

        Args:
            columns: A column name or list of column names to binarize.
            positive_value: Optional list of values to map to 1.
            negative_value: Optional list of values to map to 0.

        Raises:
            ValueError: If no dataset is loaded.
            ValueError: If only one of positive_value or negative_value is provided.
            ValueError: If unmapped values are found in a column and no default mapping is applicable.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        binarization_func(self.df, columns, positive_value, negative_value)


    def normalization(self, method: str, columns: Union[str, List[str]] = "all",
                      exclude: Optional[Union[str, List[str]]] = None) -> None:
        """
        Applies normalization to specified numerical columns using the selected method.

        This method supports three normalization strategies:
        - 'minmax': Scales values to a 0–1 range using the column's min and max.
        - 'zscore': Standardizes values based on z-score. Skips columns with zero standard deviation.
        - 'robust': Normalizes values using the formula (value - median) / IQR. Skips columns with IQR = 0.

        By default, all numerical columns are considered. Non-numerical columns are ignored.
        If `columns` is specified, only those columns are processed. If a non-numerical column
        is selected explicitly, an error is raised. Columns listed in `exclude` are ignored if
        the parameter 'columns' is used, if not, then it will be processed.

        Args:
            method: One of 'minmax', 'zscore', or 'robust'.
            columns: Optional column name or list of column names to normalize. Defaults to 'all'.
            exclude: Optional column name or list of column names to exclude from normalization.

        Raises:
            ValueError: If no dataset is loaded.
            ValueError: If an invalid method is specified.
            ValueError: If a selected column is not numeric or not found.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        if method not in ["minmax", "zscore", "robust"]:
            raise ValueError(f"Invalid method: {method}. Choose from 'minmax', 'zscore', or 'robust'.")
        normalization_func(self.df, method, columns, exclude)


    def one_hot_encoding(self, columns: Union[str, List[str]], drop_first: bool = True) -> None:
        """
        Applies one-hot encoding to specified categorical columns.

        This method replaces each specified categorical column with one or more binary
        columns (containing 0s and 1s) that represent the presence of each unique category.
        If `drop_first` is True, the first category is omitted to avoid the dummy variable trap.
        The original column(s) are removed after encoding.

        Args:
            columns: A column name or list of column names to one-hot encode.
            drop_first: Whether to drop the first category in each encoded column. Defaults to True.

        Raises:
            ValueError: If no dataset is loaded.
            ValueError: If a specified column is not found in the dataset.
            ValueError: If a specified column is not a categorical column.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        one_hot_encoding_func(self.df, columns, drop_first)


    def outlier(self, method: str, action: str, threshold: float = 3,
                columns: Union[str, List[str]] = "all") -> Union[None, pd.DataFrame]:
        """
        Performs outlier detection and handling on numerical columns using z-score or IQR.

        The method supports three actions:
        - 'detect': Returns a subset of rows considered outliers.
        - 'remove': Removes outlier rows from the dataset and prints a summary.
        - 'flag': Adds a new column called 'outlier_flag' marking outlier rows as True.

        Outliers are calculated per column using either the z-score or IQR method.
        Only numeric columns are considered. Constant-value columns are skipped automatically.
        By default, all numeric columns are used, but a specific subset can be selected.

        Args:
            method: One of 'zscore' or 'iqr'. Determines the outlier detection strategy.
            action: One of 'detect', 'remove', or 'flag'. Determines how to handle detected outliers.
            threshold: The cutoff threshold. For z-score, this is the absolute z-value (default 3).
                       For IQR, it's the multiplier applied to the IQR (default 3).
            columns: A column name, list of column names, or 'all' to apply to all numeric columns. Defaults to 'all'.

        Returns:
            pd.DataFrame or None: Returns a DataFrame of outliers if action is 'detect'. Otherwise, returns None.

        Raises:
            ValueError: If no dataset is loaded.
            ValueError: If an invalid method or action is provided.
            ValueError: If a selected column is not numeric or not found.
        """
        if self.df is None:
            raise ValueError("No dataset loaded")
        if method not in ['zscore', 'iqr']:
            raise ValueError(f"Invalid method: {method}. Choose from 'zscore' or 'iqr'.")
        if action not in ['detect', 'remove', 'flag']:
            raise ValueError(f"Invalid method: {method}. Choose from 'detect', 'remove', or 'flag'.")
        return outlier_detection(self.df, method, threshold, action, columns)
