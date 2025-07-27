# NOTE: Make sure to run this script from the same directory where 'office_dataset.csv' is located.

from cleaningbox import cleaningbox

# Initialize CleaningBox
cb = cleaningbox()

# Load dataset (with realistic missing value representations)
cb.load_data("office_dataset.csv", missingvalues=["?", "Unknown", "unknown", "Na", "None", "/", "", "Nan"])

# Preview the original dataset
print("\n--- Original Dataset ---")
cb.viewer()

print("\n--- Pre-cleaning Dataset ---")
# Check for missing values (summary mode)
cb.find_missing_values(verbose="true")

# Impute missing values
cb.imputation()

print("\n--- Column Names After Imputation ---")
# Retrieve the dataset and print its columns
print(cb.get_data().columns.tolist())

# Confirm missing values were handled
cb.find_missing_values(verbose="false")

# Binarize the 'subscribed_newsletter' column (Yes/No)
cb.binarization(columns=["subscribed_newsletter"], positive_value=["Yes"], negative_value=["No"])

# Normalize numerical columns using robust method, excluding 'Age'
cb.normalization(method="robust", columns="all", exclude="age")

# One-hot encode the 'job' column
cb.one_hot_encoding(columns="job", drop_first=True)

# Detect outliers using Z-score method and print them
outliers = cb.outlier(method="zscore", action="detect", threshold=3)
print("\n--- Detected Outliers ---")
print(outliers)

# Remove outliers
cb.outlier(method="zscore", action="remove")

print("\n--- Final Dataset Preview ---")
cb.viewer()

# Export cleaned dataset
cb.export_data("cleaned_office_dataset.csv")

print("\n✓ Cleaning complete. Cleaned dataset saved to current directory.")
