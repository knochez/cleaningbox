# CleaningBox
_A unified interface for practical data cleaning._

This document provides detailed usage examples and all valid parameter options for each public method in the 
`cleaningBox` class. For a quick start, refer to the README. This is the in-depth guide.

# Table Of Contents
- [1. Initialization](#1-initialization)
- [2. load_data()](#2-load_data)
- [3. get_data()](#3-get_data)
- [4. export_data()](#4-export_data)
- [5. viewer()](#5-viewer)
- [6. imputation()](#6-imputation)
- [7. find_missing_values()](#7-find_missing_values)
- [8. binarization()](#8-binarization)
- [9. normalization()](#9-normalization)
- [10. one_hot_encoding()](#10-one_hot_encoding)
- [11. outlier()](#11-outlier)

### 1. Initialization

To use CleaningBox, first install it using pip:
```bash
pip install cleaningbox
```

CleaningBox is designed to be used as a unified interface, rather than importing individual modules directly. 
All functionality is accessed through the main cleaningBox class:

```python
from cleaningbox import cleaningbox
```
You can then initialize it however you prefer. In this guide, the following convention will be used: 
```python
cb = cleaningbox()
```

> Note: All core methods depend on the central cleaningBox class. Importing individual files or modules directly is 
> not supported.

### 2. load_data()

The `load_data()` method loads the dataset from the selected file into the internal DataFrame.
It supports the following Excel extensions: .csv, .xlsx, .xls, and .ods, and the appropriate reader function is selected 
based on the file extension. By default, empty cells/entries are treated as 
missing values. Optionally, users may specify custom values that should also be interpreted as missing. These are 
internally converted to NaN. 

The method accepts two parameters:
```python
cb.load_data(dataset="", missingvalues=[])
```
* dataset (str): Path to the dataset file. Must be a supported format. 
* missingvalues (List): Optional list of values ( e.g., strings like 'Unknown', or numbers like 0) to treat as missing. 

Example usage:
```python
cb.load_data(dataset="office_dataset.csv", missingvalues=[-1, "Unknown"])
```
Before:
```plaintext
      Name   Age   Salary  Job Type      Car
0    Alice  29.0  70000.0  Engineer   Toyota
1      Bob  -1.0            Unknown     
2  Charlie        85000.0   Manager  Unknown
3           41.0     -1.0  Designer     Ford
```
After:
```plaintext
      Name   Age   Salary  Job Type     Car
0    Alice  29.0  70000.0  Engineer  Toyota
1      Bob   NaN      NaN       NaN     NaN
2  Charlie   NaN  85000.0   Manager     NaN
3      NaN  41.0      NaN  Designer    Ford
```

### 3. get_data()

`get_data()` returns a copy of the currently loaded dataset. This method allows users to retrieve the internal DataFrame as 
a standalone variable, or for in-line usage. Once assigned,
the dataset behaves like any standard Pandas DataFrame and can be used in external workflows, libraries,
or custom analyses.

Examples usage:
```python
df = cb.get_data()
df.head(10)
```

> Note: function chaining is supported, allowing operations without variable assignment:
```python
cb.get_data().columns.tolist()

import seaborn as sns
sns.boxplot(data=cb.get_data(), x="job", y="salary")
```

### 4. export_data()

`export_data()` exports the current dataset to a file in the specified format. 
It supports saving to .csv, .xlsx, .xls, and .ods formats. The export method is
automatically chosen based on the file extension provided. The user can also
control whether to include the index column during export.

The method accepts two parameters:
```python
cb.export_data(setFilename="", fileIndex=False/True)
```
* setFilename (str): Name of the output file, including the desired extension.
* fileIndex (bool): Whether to include the DataFrame's index in the output file. Defaults to False.

Example usage:

With fileIndex=`False`
```python
cb.export_data(setFilename="cleaned_office_dataset.xlsx", fileIndex=False)

# Exported file
#       Name   Age   Salary  Job Type     Car
# 0    Alice  29.0  70000.0  Engineer  Toyota
# 1      Bob   NaN      NaN       NaN     NaN
# 2  Charlie   NaN  85000.0   Manager     NaN
# 3      NaN  41.0      NaN  Designer    Ford
```

With fileIndex=`True`
```python
cb.export_data(setFilename="cleaned_office_dataset.xlsx", fileIndex=True)

# Exported file
#    Unnamed: 0     Name   Age   Salary  Job Type     Car
# 0           0    Alice  29.0  70000.0  Engineer  Toyota
# 1           1      Bob   NaN      NaN       NaN     NaN
# 2           2  Charlie   NaN  85000.0   Manager     NaN
# 3           3      NaN  41.0      NaN  Designer    Ford
```

### 5. viewer()
`viewer()` prints the entire dataset currently loaded in the CleaningBox instance.
This is a convenience method that displays the full DataFrame in the console,
similar to evaluating a variable directly in a notebook environment. It provides
a quick overview of the dataset without requiring export or additional setup.

Example usage:
```python
cb.viewer()

# Console output
#       Name   Age   Salary  Job Type     Car
# 0    Alice  29.0  70000.0  Engineer  Toyota
# 1      Bob   NaN      NaN       NaN     NaN
# 2  Charlie   NaN  85000.0   Manager     NaN
# 3      NaN  41.0      NaN  Designer    Ford
```

### 6. imputation()

`imputation()` performs missing value imputation on the current dataset. Applies statistical 
imputation to fill in missing values in the DataFrame. 

For numerical-entry columns,
- Uses median if the column's skewness is high (|skew| > 1), otherwise uses mean.
- Columns containing only missing values are skipped and reported.

For categorical columns:
- Uses the most frequent value (mode) to fill missing entries.
- Columns with only missing values are also skipped and reported.

Example usage:
```python
cb.imputation()
```
Before
```plaintext
      Name   Age   Salary  Job Type     Car
0    Alice  29.0  70000.0  Engineer  Toyota
1      Bob   NaN      NaN       NaN     NaN
2  Charlie   NaN  85000.0   Manager     NaN
3      NaN  41.0      NaN  Designer    Ford
```

After
```plaintext
      Name   Age   Salary  Job Type     Car
0    Alice  29.0  70000.0  Engineer  Toyota
1      Bob  35.0  77500.0  Designer    Ford
2  Charlie  35.0  85000.0   Manager    Ford
3    Alice  41.0  77500.0  Designer    Ford
```

> Note: if a column contains only NaN values, then it will be skipped and reported

Example case:
```python
cb.viewer()
# Console output:
#       Name  Age  Salary  Job Type  Car
# 0    Alice  NaN     NaN       NaN  NaN
# 1      Bob  NaN     NaN       NaN  NaN
# 2  Charlie  NaN     NaN       NaN  NaN
# 3    David  NaN     NaN       NaN  NaN

cb.imputation()
# Console output:
# ⚠️ Imputation skipped for columns with all values missing:
#   -  Skipped columns: Age, Salary, Job Type, Car
```

### 7. find_missing_values()

`find_missing_values()` checks for missing values in the dataset and provides reporting or logical feedback. 
This function scans the DataFrame for NaN (missing) values and behaves according to the
verbosity level specified:

- `"false"`: Prints a brief summary, including total missing values, affected columns,
           total cell count, and percentage of missing data.
- `"true"`: Prints the same summary as "false", plus a detailed table listing each
          column with missing values, how many are missing, and the percentage.
- `"silent"`: Suppresses all output and returns a Boolean indicating whether any
            missing values were found (True if any missing, False otherwise).

If no missing values are found, `"false"` and `"true"` print:
```plaintext
✓ Dataset is clean
```
, and `"silent"` returns False.

This method accepts one parameter:
```python
cb.find_missing_values(verbose="")
```
* verbose (str): Mode of reporting — "true", "false", or "silent" (case-insensitive). Defaults to `"false"`.

Example usage:

With verbose=`"false"`
```python
cb.find_missing_values(verbose="false")
# Console output
# ⚠️ Missing values detected
# Missing values found: 8 | Affected columns: 5
# Valid/Missing values: 20 / 8 (40.0%)
```
With verbose=`"true"`
```python
cb.find_missing_values(verbose="true")
# Console output
# ⚠️ Missing values detected
# Missing values found: 8 | Affected columns: 5
# Valid/Missing values: 20 / 8 (40.0%)
# 
#   Attribute_Name  Missing_Value_Count  Missing_Value_Percentage
# 0            Age                    2                      50.0
# 1            Car                    2                      50.0
# 2         Salary                    2                      50.0
# 3           Name                    1                      25.0
# 4       Job Type                    1                      25.0
```
With verbose=`"silent"`
```python
if cb.find_missing_values(verbose="silent"):
    print("Missing data found")
else:
    print("Dataset is clean")
# Console output
# Missing data found
```
### 8. binarization()
`binarization()` converts categorical values in specified columns into binary form (0/1).
By default, this method maps the string "yes" to 1 and "no" to 0 (case-sensitive). The user
can override this by specifying custom lists of values to be treated as
positive (1) and negative (0). All other values will trigger an error unless
explicitly handled.

This method takes one mandatory and two optional parameters:
```python
cb.binarization(columns=[], positive_value=[], negative_value=[])
```
* columns (List[str]): List of column/s to apply binarization to.
* positive_value (Optional[List[str]]): Values to be mapped to 1.
* negative_value (Optional[List[str]]): Values to be mapped to 0.

Example usage:

With default mapping:
```python
cb.viewer()
# Console output
#       Name  Age  Salary    Job Type      Car Remote Full Time
# 0    Alice   29   70000    Engineer   Toyota    yes        no
# 1      Bob   34   60000  Technician    Honda     no        no
# 2  Charlie   45   85000     Manager     Ford    yes        no
# 3    David   41   78000    Designer      BMW     no       yes

cb.binarization(columns=["Remote", "Full Time"])
cb.viewer()
# Console output
#       Name  Age  Salary    Job Type      Car  Remote  Full Time
# 0    Alice   29   70000    Engineer   Toyota       1          0
# 1      Bob   34   60000  Technician    Honda       0          0
# 2  Charlie   45   85000     Manager     Ford       1          0
# 3    David   41   78000    Designer      BMW       0          1
```
With custom mapping:
```python
cb.viewer()
# Console output
#       Name  Age  Salary    Job Type      Car Remote Full Time
# 0    Alice   29   70000    Engineer   Toyota    yes        no
# 1      Bob   34   60000  Technician    Honda     no        no
# 2  Charlie   45   85000     Manager     Ford    yes        no
# 3    David   41   78000    Designer      BMW     no       yes

cb.binarization(columns=["Job Type", "Car"], 
                positive_value=["Engineer", "Honda", "Ford"], 
                negative_value=["Technician", "Manager", "Designer", "Toyota", "BMW"])
cb.viewer()
# Console output
#       Name  Age  Salary  Job Type  Car Remote Full Time
# 0    Alice   29   70000         1    0    yes        no
# 1      Bob   34   60000         0    1     no        no
# 2  Charlie   45   85000         0    1    yes        no
# 3    David   41   78000         0    0     no       yes
```
When using custom mapping, all unique values in the selected column/s must be used, otherwise, an error
will be raised:
```python
cb.binarization(columns=['Job Type'], positive_value=["Engineer"], negative_value=["Manager"])
# Console output
# ValueError: Column 'Job Type' contains unmapped values: {'Designer', 'Technician'}
```

### 9. normalization()

`normalization()` scales numerical columns using one of three normalization methods. It is typically used to bring 
features into a comparable range or distribution, which is especially useful before modeling or analysis.

Supported methods:

* "minmax": Scales values to a 0–1 range using the column’s min and max.

* "zscore": Standardizes values using z-score. Columns with zero standard deviation are skipped.

* "robust": Scales using the formula (value - median) / IQR. Skips columns with IQR = 0.

This method accepts one required and two optional parameters:

```python
cb.normalization(method="", columns="all", exclude=None)
```
* method (str): Normalization strategy — "minmax", "zscore", or "robust" (required).

* columns (str | List[str]): Columns to normalize. Defaults to "all". Non-numerical columns will 
raise an error if selected.

* exclude (str | List[str] | None): Optional. Columns to skip only when using "all" mode. 
If specific columns are targeted with columns=, then exclude will be ignored (without error).

Example usage

Selecting `all` columns, and using `minmax` as the method:
```python
cb.viewer()
# Console output
#   Customer Type Department Job Level  Salary  YAC  Sick Days Taken
# 0    Individual         HR    Senior  110989    4                4
# 1    Individual  Marketing    Senior   36230    1                4
# 2     Corporate    Finance    Senior  114354   13               11
# 3     Corporate  Marketing       Mid  101323   21               11
# 4     Corporate  Marketing    Junior  113820   19                3

cb.normalization(method="minmax")
cb.viewer()
# Console output
#   Customer Type Department Job Level    Salary   YAC  Sick Days Taken
# 0    Individual         HR    Senior  0.956927  0.15            0.125
# 1    Individual  Marketing    Senior  0.000000  0.00            0.125
# 2     Corporate    Finance    Senior  1.000000  0.60            1.000
# 3     Corporate  Marketing       Mid  0.833201  1.00            1.000
# 4     Corporate  Marketing    Junior  0.993165  0.90            0.000
```

Selecting `all` columns, using `zscore` method, but `excluding` specified columns: 
```python
cb.normalization(method='zscore', exclude=['YAC', "Sick Days Taken"])
cb.viewer()
# Console output
#   Customer Type Department Job Level    Salary  YAC  Sick Days Taken
# 0    Individual         HR    Senior  0.467627    4                4
# 1    Individual  Marketing    Senior -1.766794    1                4
# 2     Corporate    Finance    Senior  0.568201   13               11
# 3     Corporate  Marketing       Mid  0.178726   21               11
# 4     Corporate  Marketing    Junior  0.552240   19                3
```

Selecting `specified` columns, using `robust` method, but `excluding` specified columns:
```python
cb.normalization(method='robust', columns=['YAC', 'Salary'], exclude="Sick Days Taken")
cb.viewer()
# Console output
#   Customer Type Department Job Level    Salary       YAC  Sick Days Taken
# 0    Individual         HR    Senior  0.000000 -0.600000                4
# 1    Individual  Marketing    Senior -5.982156 -0.800000                4
# 2     Corporate    Finance    Senior  0.269265  0.000000               11
# 3     Corporate  Marketing       Mid -0.773466  0.533333               11
# 4     Corporate  Marketing    Junior  0.226534  0.400000                3
```
> Note: When specifying columns explicitly, `exclude` is not required. If provided, it will 
> be ignored without error.


### 10. one_hot_encoding()

`one_hot_encoding()` applies one-hot encoding to specified categorical columns. 
This method replaces each specified categorical column with one or more binary
columns (containing 0s and 1s) that represent the presence of each unique category.
If `drop_first` is True, the first category is omitted to avoid the dummy variable trap.
The original column(s) are removed after encoding.

This method accepts one required and one optional parameter:
```python
cb.one_hot_encoding(columns="", drop_first=True/False)
```
* columns (Union[str, List[str]]): Column name or list of categorical columns to encode.
* drop_first (bool): If True, drops the first category in each encoded column. Defaults to True.

Example usage

With `drop_first=True`:
```python
cb.viewer()
# Console output
#   Department
# 0         HR
# 1  Marketing
# 2    Finance
# 3  Marketing
# 4  Marketing

cb.one_hot_encoding(columns=["Department"])
cb.viewer()
# Console output
#    Department_HR  Department_Marketing
# 0              1                     0
# 1              0                     1
# 2              0                     0
# 3              0                     1
# 4              0                     1
```

With `drop_first=False`:
```python
cb.one_hot_encoding(columns=["Department"], drop_first=False)
cb.viewer()
# Console output
#    Department_Finance  Department_HR  Department_Marketing
# 0                   0              1                     0
# 1                   0              0                     1
# 2                   1              0                     0
# 3                   0              0                     1
# 4                   0              0                     1
```

### 11. outlier()
`outlier()` identifies and handles outliers in numeric columns using z-score or IQR methods.

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
- Columns with constant values (std_dev=0 or IQR=0) are skipped with a message.
- If `columns` is set to "all", all numeric columns are included unless specified otherwise.
- If the specified `columns` include a non-numeric or missing column/value, an error is raised.
- The result is either returned (for "detect") or applied in-place (for "remove" and "flag").

This method accepts two required and two optional parameters:
```python
cb.outlier(method="", action="", threshold=N, columns="")
```

* method (str): Outlier detection method — either "zscore" or "iqr".
* action (str): Handling strategy — "detect", "remove", or "flag".
* threshold (float): Sensitivity threshold. Higher values reduce sensitivity (optional). Defaults to 3.
* columns (Union[str, List[str]]): Target columns for outlier detection (optional). Defaults to "all".

Example usage
With method=`"zscore"` and action=`"detect"`
```python
cb.viewer()
# Console output
#       age           job   marital  ... No. employed Term Deposit State
# 0      31   blue-collar  divorced  ...       5191.0            0   ACT
# 1      39        admin.   married  ...       5076.2            0   ACT
# 2      47  entrepreneur   married  ...       5017.5            0   TAS
# 3      55   blue-collar  divorced  ...       5176.3            0    WA
# 4      28  entrepreneur   married  ...       5176.3            1   NSW
# ...   ...           ...       ...  ...          ...          ...   ...
# 2631   24        admin.    single  ...       4963.6            0   VIC
# 2632   38   blue-collar   married  ...       4963.6            0   ACT
# 2633   32    technician    single  ...       5195.8            0   QLD
# 2634   39        admin.   married  ...       5228.1            1   VIC
# 2635   35    technician    single  ...       5228.1            0    WA
# 
# [2636 rows x 22 columns]

print(cb.outlier(method="zscore", action="detect"))
# Console output
#       age           job   marital  ... No. employed Term Deposit State
# 4      28  entrepreneur   married  ...       5176.3            1   NSW
# 11     43      services   married  ...       4991.6            0    WA
# 41     25      services    single  ...       4991.6            0   QLD
# 63     41    management  divorced  ...       5008.7            0    SA
# 73     53        admin.   married  ...       4991.6            0    NT
# ...   ...           ...       ...  ...          ...          ...   ...
# 2607   83     housemaid  divorced  ...       5176.3            1    SA
# 2615   60       retired   married  ...       5099.1            1   QLD
# 2623   33        admin.    single  ...       4963.6            1   VIC
# 2628   49  entrepreneur   married  ...       5008.7            1   NSW
# 2634   39        admin.   married  ...       5228.1            1   VIC
# 
# [240 rows x 22 columns]
```

With method=`"iqr"`, action=`"remove"`, and threshold=`1.5`
```python
cb.outlier(method="iqr", action="remove", threshold=1.5)
# Console output
# 883 rows containing outliers have been successfully removed
```

method=`zscore`, action=`flag`, threshold=`2`, columns=`passed days`
```python
cb.outlier(method="zscore", action="flag", threshold=3, columns="passed days")
# Console output
#       age           job   marital  ... Term Deposit State outlier_flag
# 0      31   blue-collar  divorced  ...            0   ACT        True
# 1      39        admin.   married  ...            0   ACT        False
# 2      47  entrepreneur   married  ...            0   TAS         True
# 3      55   blue-collar  divorced  ...            0    WA         True
# 4      28  entrepreneur   married  ...            1   NSW        False
# ...   ...           ...       ...  ...          ...   ...          ...
# 2631   24        admin.    single  ...            0   VIC         True
# 2632   38   blue-collar   married  ...            0   ACT        False
# 2633   32    technician    single  ...            0   QLD        False
# 2634   39        admin.   married  ...            1   VIC         True
# 2635   35    technician    single  ...            0    WA         True
```
> If the 'outlier_flag' column already exists, it will be overwritten and 
> the following warning will be displayed:
> * Warning: 'outlier_flag' column already exists and will be overwritten.
