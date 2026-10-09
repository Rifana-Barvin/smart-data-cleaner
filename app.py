import streamlit as st
import pandas as pd
from io import BytesIO
from cleaner import clean_data


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Smart Data Cleaner",
    page_icon="🧹",
    layout="wide"
)

# ---------------- PROFESSIONAL UI STYLING ----------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    h1 {
        color: #17365D;
        font-weight: 750;
    }

    h2, h3 {
        color: #24476B;
    }

    [data-testid="stMetric"] {
        background-color: #F0F6FF;
        border: 1px solid #D8E6F7;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #425466;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #174EA6;
    }

    div.stButton > button[kind="primary"] {
        background-color: #1769AA;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #0F4C81;
        color: white;
    }

    div[data-testid="stFileUploader"] {
        border: 1px dashed #A9C7E8;
        border-radius: 10px;
        padding: 10px;
        background-color: #F8FBFF;
    }

    hr {
        border-color: #DCE5EF;
    }
</style>
""", unsafe_allow_html=True)


st.title("🧹 Smart Data Cleaner")
st.write(
    "Clean messy datasets, generate cleaning reports, "
    "and analyze your sales data."
)

st.divider()


# ---------------- FILE UPLOAD ----------------

st.header("📁 Upload Your Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        # Read the uploaded file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Original Dataset")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Original Rows", len(df))

        with col2:
            st.metric("Original Columns", len(df.columns))

        st.dataframe(df, use_container_width=True)

        st.divider()

        # ---------------- CLEAN DATA ----------------

        if st.button("🧹 Clean Data", type="primary"):

            cleaned_df, report = clean_data(df)

            st.session_state["cleaned_df"] = cleaned_df
            st.session_state["cleaning_report"] = report
            st.session_state["source_name"] = uploaded_file.name

        # Show results if cleaning has been completed
        if (
            "cleaned_df" in st.session_state
            and st.session_state.get("source_name") == uploaded_file.name
        ):

            cleaned_df = st.session_state["cleaned_df"]
            report = st.session_state["cleaning_report"]

            # ---------------- CLEANING REPORT ----------------

            st.header("✅ Data Cleaning Report")

            missing_before = report.get("Missing Values Before", 0)
            missing_after = report.get("Missing Values After", 0)

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric(
                "Original Rows",
                report.get("Original Rows", len(df))
            )

            metric2.metric(
                "Cleaned Rows",
                report.get("Cleaned Rows", len(cleaned_df))
            )

            metric3.metric(
                "Missing Values Fixed",
                max(0, missing_before - missing_after)
            )

            metric4.metric(
                "Duplicates Removed",
                report.get("Duplicates Removed", 0)
            )

            report_df = pd.DataFrame({
                "Cleaning Operation": list(report.keys()),
                "Result": list(report.values())
            })

            st.dataframe(report_df, use_container_width=True)

            st.subheader("Cleaned Dataset")
            st.dataframe(cleaned_df, use_container_width=True)

            # ---------------- DOWNLOAD FILES ----------------

            st.subheader("📥 Download Cleaned Data")

            download1, download2 = st.columns(2)

            with download1:
                csv_data = cleaned_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="cleaned_data.csv",
                    mime="text/csv"
                )

            with download2:
                excel_buffer = BytesIO()

                with pd.ExcelWriter(
                    excel_buffer,
                    engine="openpyxl"
                ) as writer:
                    cleaned_df.to_excel(
                        writer,
                        index=False,
                        sheet_name="Cleaned Data"
                    )

                st.download_button(
                    label="Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name="cleaned_data.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )
                )

            # ---------------- SALES ANALYTICS ----------------

            st.divider()
            st.header("📊 Sales Analytics Dashboard")

            required_columns = {
                "Purchase_Amount",
                "Product",
                "City",
                "Customer_ID",
                "Purchase_Date"
            }

            if required_columns.issubset(cleaned_df.columns):

                sales_df = cleaned_df.copy()

                sales_df["Purchase_Amount"] = pd.to_numeric(
                    sales_df["Purchase_Amount"],
                    errors="coerce"
                )

                sales_df["Purchase_Date"] = pd.to_datetime(
                    sales_df["Purchase_Date"],
                    errors="coerce"
                )

                sales_df = sales_df.dropna(
                    subset=["Purchase_Amount"]
                )

                if not sales_df.empty:

                    # ---------------- FILTERS ----------------

                    st.subheader("🔎 Filter Sales Data")

                    filter1, filter2 = st.columns(2)

                    with filter1:
                        products = sorted(
                            sales_df["Product"]
                            .dropna()
                            .astype(str)
                            .unique()
                            .tolist()
                        )

                        selected_product = st.selectbox(
                            "Select Product",
                            ["All Products"] + products
                        )

                    with filter2:
                        cities = sorted(
                            sales_df["City"]
                            .dropna()
                            .astype(str)
                            .unique()
                            .tolist()
                        )

                        selected_city = st.selectbox(
                            "Select City",
                            ["All Cities"] + cities
                        )

                    # Apply filters
                    filtered_df = sales_df.copy()

                    if selected_product != "All Products":
                        filtered_df = filtered_df[
                            filtered_df["Product"].astype(str)
                            == selected_product
                        ]

                    if selected_city != "All Cities":
                        filtered_df = filtered_df[
                            filtered_df["City"].astype(str)
                            == selected_city
                        ]

                    if not filtered_df.empty:

                        # ---------------- KEY METRICS ----------------

                        total_sales = filtered_df[
                            "Purchase_Amount"
                        ].sum()

                        average_purchase = filtered_df[
                            "Purchase_Amount"
                        ].mean()

                        total_customers = filtered_df[
                            "Customer_ID"
                        ].nunique()

                        product_sales = (
                            filtered_df.groupby("Product")[
                                "Purchase_Amount"
                            ]
                            .sum()
                            .sort_values(ascending=False)
                        )

                        city_sales = (
                            filtered_df.groupby("City")[
                                "Purchase_Amount"
                            ]
                            .sum()
                            .sort_values(ascending=False)
                        )

                        top_product = (
                            product_sales.idxmax()
                            if not product_sales.empty
                            else "N/A"
                        )

                        st.subheader("💰 Business Overview")

                        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

                        kpi1.metric(
                            "Total Sales",
                            f"₹{total_sales:,.2f}"
                        )

                        kpi2.metric(
                            "Average Purchase",
                            f"₹{average_purchase:,.2f}"
                        )

                        kpi3.metric(
                            "Unique Customers",
                            total_customers
                        )

                        kpi4.metric(
                            "Top Product",
                            str(top_product)
                        )

                        # ---------------- PRODUCT CHART ----------------

                        st.divider()
                        st.subheader("🛍️ Product-wise Sales")

                        st.bar_chart(product_sales)

                        # ---------------- CITY CHART ----------------

                        st.subheader("📍 City-wise Sales")

                        st.bar_chart(city_sales)

                        # ---------------- SALES TREND ----------------

                        st.subheader("📈 Sales Trend Over Time")

                        dated_sales = filtered_df.dropna(
                            subset=["Purchase_Date"]
                        )

                        if not dated_sales.empty:

                            daily_sales = (
                                dated_sales.groupby("Purchase_Date")[
                                    "Purchase_Amount"
                                ]
                                .sum()
                                .sort_index()
                            )

                            st.line_chart(daily_sales)

                        else:
                            st.info(
                                "No valid purchase dates are available "
                                "for the sales trend."
                            )

                        # ---------------- FILTERED DATA ----------------

                        with st.expander("View Filtered Sales Records"):
                            st.dataframe(
                                filtered_df,
                                use_container_width=True
                            )

                        st.caption(
                            f"Showing {len(filtered_df)} of "
                            f"{len(sales_df)} sales records."
                        )

                    else:
                        st.warning(
                            "No records match your selected filters. "
                            "Try selecting another product or city."
                        )

                else:
                    st.warning(
                        "No valid purchase amounts are available "
                        "for sales analysis."
                    )

            else:
                st.info(
                    "Sales analytics requires these columns: "
                    + ", ".join(sorted(required_columns))
                )


    except Exception as e:
        st.error(f"Unable to process the file: {e}")

else:
    st.info("Upload a CSV or Excel file to get started.")
