# CleaningBox
_A unified interface for practical data cleaning._

[![Python Version](https://img.shields.io/pypi/pyversions/cleaningbox.svg)](https://pypi.org/project/cleaningbox/)
[![PyPI version](https://img.shields.io/pypi/v/cleaningbox.svg)](https://pypi.org/project/cleaningbox/)
[![License](https://img.shields.io/github/license/knochez/cleaningbox)](https://github.com/knochez/cleaningbox/blob/main/LICENSE)


**CleaningBox** is a lightweight, modular Python library that streamlines data cleaning for structured (tabular) datasets. It provides a simple, readable interface for handling common preprocessing tasks such as missing value imputation, encoding, normalization, and outlier detection — all in one place.

Designed for clarity and flexibility, CleaningBox helps you prepare data efficiently for analysis or machine learning workflows, without unnecessary boilerplate.

## Changelog V1.0.3:
> Note: Versions 1.0.0 to 1.0.2 were removed due to early development cleanup. This is the first official release.

## Features

| 🔧 **Functionality**        | 📄 **Description**                                                | 🎯 **Purpose / Output**                                                 |
|-----------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------------|
| 🔍 Missing Value Detection  | Scans for missing values, with adjustable feedback verbosity      | Returns summary, detailed table, or a Boolean (for automation)          |
| 🧩 Missing Value Imputation | Fills missing values using statistical strategies                 | Uses mean/median/mode based on data skewness and column type            |
| 📐 Normalization            | Scales numeric data using `min-max`, `z-score`, or `robust`       | Standardizes data for modeling or comparisons                           |
| 0️⃣1️⃣ Binarization         | Converts yes/no, or user-specified, values into binary 0/1 format | Simplifies categorical values for analysis or ML input                  |
| 📦 One-Hot Encoding         | Encodes categorical variables into multiple binary columns        | Prepares data for ML algorithms that can't handle text categories       |
| 🚨 Outlier Detection        | Detects/flags and/or removes outliers using `z-score` or `IQR`    | Can return, remove, or flag outlier rows                                |
| 🖥️ Data Preview            | Displays a clean, tabular printout of the current dataset         | Prints a readable Pandas DataFrame snapshot                             |
| 💾 Export Data              | Saves the current dataset to a selected file extension            | Useful for sharing or downstream workflows                              |
| 🔓 Data Access              | Returns dataset as a standard Pandas DataFrame                    | Allows integration with external tools like Seaborn, Scikit-learn, etc. |

## Installation

CleaningBox is available on [PyPI](https://pypi.org/cleaningbox), so you can install it using pip:
> **Requires**: Python 3.7 or higher
```bash
pip install cleaningbox
```

### Installing from Source (for Development)

To install the latest version directly from the repository:

1. Clone the repository from GitHub
2. Navigate to the project directory
3. Install the package in editable mode using pip

## Usage

📘 For full in-depth documentation, see the [Full Documentation](https://github.com/knochez/cleaningbox/blob/main/doc.md).


### Basic Example

```python
from cleaningbox import cleaningbox

cb = cleaningbox()
cb.load_data("office_dataset.csv", missingvalues=["?", "NaN", "None", "/"])
cb.find_missing_values(verbose="true")
# Output
# ⚠️ Missing values detected
# Missing values found: 8 | Affected columns: 3
# Valid/Missing values: 210 / 8 (3.81%)
# 
#       Attribute_Name  Missing_Value_Count  Missing_Value_Percentage
# 0             salary                    3                      10.0
# 1              job                      3                      10.0
# 2  subscribed_newsletter                2                       6.7

cb.imputation()
cb.viewer()
# Output
#        name   age      job   salary  subscribed_newsletter
# 0   Alice    34.0  Manager  55000.0                   Yes
# 1   Bob      45.0  Analyst  62000.0                   No
# ...
```

### Full Cleaning Workflow
```python
# Encode binary column
cb.binarization(columns=["subscribed_newsletter"])

# Normalize data (exclude age)
cb.normalization(method="robust", columns="all", exclude="age")

cb.one_hot_encoding(columns="job", drop_first=True)

# Flag outliers
cb.outlier(method="zscore", action="flag", threshold=3)

# Export cleaned dataset
cb.export_data("cleaned_office_dataset.csv")
```

### 🧪 Combine with Pandas or ML libraries
```python
import seaborn as sns

# Retrieve as a native Pandas DataFrame
df = cb.get_data()
sns.boxplot(data=df, x="job_Sales", y="salary")
```
✅ For a full working demo, see the demo/example.py script.

📘 For full in-depth documentation, see the [Full Documentation](https://github.com/knochez/cleaningbox/blob/main/doc.md).


## 🤝 Contributing

Contributions are welcome! If you'd like to fix a bug, add a feature, or improve documentation:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a pull request

Please ensure code style and functionality are consistent with the existing codebase.


## 📬 Support & Feedback

Have questions, bugs, or suggestions?

- 🐛 [Submit an issue](https://github.com/knochez/cleaningbox/issues) on GitHub
- 💬 For feature requests or general feedback, feel free to open a discussion or contribute.

## 👤 Author

**Kevin Nochez** | [GitHub Account](https://github.com/knochez)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.