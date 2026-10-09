import pandas as pd
from cleaner import clean_data


# ==========================================
# READ DATASET
# ==========================================

df = pd.read_csv(
    "messy_customer_sales_dataset.csv"
)


# ==========================================
# BEFORE CLEANING
# ==========================================

print("\nBEFORE CLEANING")
print("=" * 50)

print(df)

print("\nMissing values:")
print(df.isnull().sum())


# ==========================================
# CLEAN DATA
# ==========================================

cleaned_df, report = clean_data(df)


# ==========================================
# AFTER CLEANING
# ==========================================

print("\n\nAFTER CLEANING")
print("=" * 50)

print(cleaned_df)

print("\nMissing values:")
print(cleaned_df.isnull().sum())


# ==========================================
# CLEANING REPORT
# ==========================================

print("\n\nDATA CLEANING REPORT")
print("=" * 50)

for item, value in report.items():
    print(f"{item:<25}: {value}")


# ==========================================
# SAVE CLEANED DATA
# ==========================================

cleaned_df.to_csv(
    "cleaned_customer_sales.csv",
    index=False
)


print("\nCleaned file saved successfully!")