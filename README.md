# Smart Data Cleaner & Sales Analytics Dashboard

A Python-based web application that cleans messy datasets, generates cleaning reports, and provides an interactive dashboard for sales analysis.

## Features

- Upload CSV and Excel files
- Remove duplicate rows
- Handle missing values
- Standardize text and date formats
- Generate a data cleaning report
- Download cleaned data in CSV and Excel formats
- Display key sales metrics
- Filter sales by product and city
- Visualize product-wise and city-wise sales
- Analyze sales trends over time

## Technologies Used

- Python
- Pandas
- Streamlit
- OpenPyXL

## Project Structure

```text
SmartDataCleaner/
├── app.py
├── cleaner.py
├── test_cleaner.py
├── requirements.txt
├── messy_customer_sales_dataset.csv
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd SmartDataCleaner
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## How to Use

1. Upload a CSV or Excel dataset.
2. Click **Clean Data**.
3. Review the cleaning report and cleaned dataset.
4. Download the cleaned file.
5. Explore the sales dashboard using the product and city filters.

## Sample Dataset

The included sample dataset contains customer and sales information with intentional data-quality issues for testing the cleaning process.

## Screenshots

Screenshots of the application will be added here.
<img width="1428" height="650" alt="image" src="https://github.com/user-attachments/assets/9fcc5f6f-ffa2-4ebb-b31d-fb205d278c97" />
<img width="1495" height="1002" alt="image" src="https://github.com/user-attachments/assets/56279b20-7c59-4a7d-ae72-d79ed9786a15" />
<img width="1330" height="956" alt="image" src="https://github.com/user-attachments/assets/ada15405-428d-4b25-b9f1-e83f725a5a38" />
<img width="1390" height="660" alt="image" src="https://github.com/user-attachments/assets/b16cda1e-616c-4aef-8a61-338799ee4bf8" />
<img width="1571" height="971" alt="image" src="https://github.com/user-attachments/assets/4885b01e-d07e-41e0-9a7c-20d77719ab16" />
<img width="1055" height="937" alt="image" src="https://github.com/user-attachments/assets/a9042c10-2365-40b1-8323-c27cf09c383a" />
<img width="1226" height="970" alt="image" src="https://github.com/user-attachments/assets/7c1bd489-e48a-4e7e-8625-48d49ee43f92" />


## Future Improvements

- More data validation options
- Additional interactive visualizations
- Enhanced dashboard design
- Online deployment

## Author

Developed as a Python, data cleaning, and analytics portfolio project.

