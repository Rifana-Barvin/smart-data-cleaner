"""
Smart Data Cleaner
------------------
Reusable data-cleaning module for CSV and Excel files.

Features:
- Removes duplicate records
- Handles missing numerical values
- Removes unnecessary spaces
- Standardizes text values
- Removes records with missing names
"""

import pandas as pd


def clean_data(df):
    """
    Cleans and standardizes customer sales data.
    Returns the cleaned dataframe and cleaning report.
    """

    # ---------------------------------------------
    # Initial information
    # ---------------------------------------------
    original_rows = len(df)

    missing_before = df.isnull().sum().sum()

    # Create a copy so original data is not modified
    df = df.copy()

    # ---------------------------------------------
    # 1. Remove completely duplicate rows
    # ---------------------------------------------
    rows_before_duplicates = len(df)

    df = df.drop_duplicates()

    duplicates_removed = (
        rows_before_duplicates - len(df)
    )

    # ---------------------------------------------
    # 2. Clean column names
    # ---------------------------------------------
    df.columns = df.columns.str.strip()

    # ---------------------------------------------
    # 3. Remove extra spaces from text columns
    # ---------------------------------------------
    text_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    # ---------------------------------------------
    # 4. Standardize city names
    # ---------------------------------------------
    if "City" in df.columns:
        df["City"] = df["City"].str.title()

    # ---------------------------------------------
    # 5. Convert Age to numeric
    # ---------------------------------------------
    age_missing_before = 0

    if "Age" in df.columns:

        age_missing_before = df["Age"].isnull().sum()

        df["Age"] = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

        df["Age"] = df["Age"].fillna(
            df["Age"].median()
        )

    # ---------------------------------------------
    # 6. Convert Purchase Amount to numeric
    # ---------------------------------------------
    amount_missing_before = 0

    if "Purchase_Amount" in df.columns:

        amount_missing_before = (
            df["Purchase_Amount"].isnull().sum()
        )

        df["Purchase_Amount"] = pd.to_numeric(
            df["Purchase_Amount"],
            errors="coerce"
        )

        df["Purchase_Amount"] = (
            df["Purchase_Amount"].fillna(
                df["Purchase_Amount"].median()
            )
        )

    # ---------------------------------------------
    # 7. Standardize Purchase Date
    # ---------------------------------------------
    invalid_dates = 0

    if "Purchase_Date" in df.columns:

        df["Purchase_Date"] = (
            df["Purchase_Date"]
            .astype(str)
            .str.strip()
        )

        date_formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%m-%d-%Y",
            "%m/%d/%Y",
            "%B %d, %Y",
            "%b %d, %Y"
        ]

        converted_dates = pd.Series(
            pd.NaT,
            index=df.index
        )

        for date_format in date_formats:

            mask = converted_dates.isna()

            converted_dates.loc[mask] = (
                pd.to_datetime(
                    df.loc[mask, "Purchase_Date"],
                    format=date_format,
                    errors="coerce"
                )
            )

        df["Purchase_Date"] = converted_dates

        invalid_dates = df["Purchase_Date"].isnull().sum()

    # ---------------------------------------------
    # 8. Remove rows with missing Name
    # ---------------------------------------------
    if "Name" in df.columns:
        df = df.dropna(
            subset=["Name"]
        )

    # ---------------------------------------------
    # 9. Reset index
    # ---------------------------------------------
    df = df.reset_index(drop=True)

    # ---------------------------------------------
    # Final information
    # ---------------------------------------------
    cleaned_rows = len(df)

    missing_after = df.isnull().sum().sum()

    # ---------------------------------------------
    # Create cleaning report
    # ---------------------------------------------
    report = {
        "Original Rows": original_rows,
        "Cleaned Rows": cleaned_rows,
        "Duplicates Removed": duplicates_removed,
        "Missing Ages Fixed": age_missing_before,
        "Missing Amounts Fixed": amount_missing_before,
        "Invalid Dates": invalid_dates,
        "Missing Values Before": missing_before,
        "Missing Values After": missing_after
    }
    return df, report