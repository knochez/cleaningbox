import pandas as pd

data = {
    "name": [
        "Alice Smith", "Bob Johnson", "Cathy Nguyen", "David Lee", "Ella Carter", "Frank Wright",
        "Grace Kim", "Henry Adams", "Isla Morgan", "Jack Brown", "Karen White", "Leo Davis",
        "Mia Thompson", "Nathan Scott", "Olivia Brooks", "Paul Walker", "Quincy Allen", "Rachel Fox",
        "Steve Nash", "Tina Blake", "Uma Reed", "Victor Hale", "Wendy Price", "Xander Moon",
        "Yasmin Ortiz", "Zack Cole", "Ann Young", "Ben Ford", "Cara Grant", "Dean Blake"
    ],
    "age": [
        34, 45, 29, 42, 50, 37, "?", 41, 36, 38, "unknown", 28, 33, "Na", 49,
        31, "None", 46, 35, 40, 39, "/", 27, 32, 36, "NaN", 30, 38, "Unknown", 43
    ],
    "job": [
        "Admin Assistant", "IT Technician", "HR Manager", "Warehouse Clerk", "Admin Assistant",
        "IT Technician", "Admin Assistant", "/", "Customer Service", "HR Manager", "Admin Assistant",
        "unknown", "IT Technician", "Warehouse Clerk", "HR Manager", "Customer Service", "NaN",
        "Admin Assistant", "IT Technician", "None", "HR Manager", "Customer Service", "Admin Assistant",
        "Warehouse Clerk", "Unknown", "IT Technician", "Admin Assistant", "HR Manager", "Na", "Admin Assistant"
    ],
    "marital_status": [
        "Married", "Single", "Married", "Divorced", "Single", "Married", "?", "Divorced", "Married", None,
        "Single", "Na", "Divorced", "Unknown", "Married", "Single", "unknown", "Single", "Divorced", "Married",
        "/", "Married", "Single", "NaN", "Single", "Divorced", "Single", "Unknown", "Married", "None"
    ],
    "education": [
        "University Degree", "High School", "Basic 9 Years", "Basic 6 Years", "High School",
        "University Degree", "Unknown", "Basic 9 Years", "Illiterate", "Basic 6 Years", "Basic 9 Years",
        "University Degree", "High School", "Na", "Basic 6 Years", "Illiterate", "unknown",
        "High School", "Basic 9 Years", "/", "Illiterate", "NaN", "Basic 6 Years", "Unknown",
        "High School", "University Degree", "Illiterate", "High School", "Na", "None"
    ],
    "salary": [
        55000, 62000, 48000, "None", 51000, 63000, 54000, 58000, 49000, "?", "Unknown", 56000,
        "unknown", "Na", 53000, 61000, 52000, "NaN", "None", 50000, "/", "Na", "54000", "59000",
        "60000", 57000, 62000, "Unknown", 51000, 55000
    ],
    "subscribed_newsletter": [
        "Yes", "No", "Yes", "No", "Yes", None, "No", "No", "Yes", "Yes", "Unknown", "No",
        "Yes", "Na", "No", "Yes", "/", "unknown", "No", "Yes", "NaN", "No", "Yes", "Yes",
        "None", "Yes", "No", "No", "Yes", "Unknown"
    ]
}

df = pd.DataFrame(data)
df.to_csv("office_dataset.csv", index=False)
