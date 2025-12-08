📊 CSV to XLSX Data Cleaning Tool

A command-line Python tool for reading CSV files, cleaning & normalizing data, and exporting the results to Excel (.xlsx).
Designed for data preparation, automation, and report generation.

This tool supports:

Reading one or multiple CSV files

Normalizing column names automatically

Cleaning string fields (trim whitespace)

Handling missing values

Parsing date columns (manual or auto-detect)

Renaming columns from CLI

Simple logging & error handling

Exporting clean data to .xlsx (OpenPyXL)

🚀 Features
✔ Read & Combine CSVs

Pass one or many CSV files → tool merges into a single DataFrame.

✔ Normalize Column Names

Converts column headers into clean, consistent snake_case.

✔ Parse Dates Automatically

Auto-detects date/time columns OR let users specify.

✔ Handle Missing Values

Drop empty rows

Drop rows with ANY missing values

Drop rows below threshold (--dropna-thresh)

Fill missing values with user-defined value

✔ Rename Columns via CLI

Example:

--rename "Old Name:new_name,Total Price:total"

✔ Export to Excel (.xlsx)

Uses pandas + openpyxl

No index column in output

✔ Logging

Info, warnings, and error messages for invalid files, bad columns, and processing issues.

📦 Installation
1. Clone the repository
git clone <your_repo_url>
cd csv_to_xlsx

2. Install dependencies
pip install -r requirements.txt

▶️ Usage
Basic conversion
python data_prep.py -i data.csv -o output.xlsx

Multiple CSVs merged
python data_prep.py -i jan.csv feb.csv mar.csv -o q1.xlsx

Parse specific date columns
python data_prep.py -i sales.csv -o cleaned.xlsx --date-cols order_date,ship_date

Auto-detect date columns

(Just omit --date-cols)

Rename columns
python data_prep.py -i raw.csv -o cleaned.xlsx --rename "Order ID:order_id,Total Amount:total"

Fill missing values
python data_prep.py -i data.csv -o out.xlsx --fillna 0

Drop rows with ANY missing values
python data_prep.py -i data.csv -o out.xlsx --dropna-any

Keep rows with at least N non-null values
python data_prep.py -i data.csv -o out.xlsx --dropna-thresh 3

Verbose logging
python data_prep.py -i data.csv -o out.xlsx --verbose

🔍 Output Example

After cleaning, output will be an Excel file:

output.xlsx


Cleaned data includes:

Normalized column names

Trimmed string values

Parsed date formats

Missing values resolved

Renamed columns (if specified)

📁 Project Structure
csv_to_xlsx/
├── data_prep.py
├── requirements.txt
└── README.md

🛠 Technologies Used

Python 3

Pandas

OpenPyXL

Argparse

Logging

📝 Example Command
python data_prep.py -i sales_jan.csv sales_feb.csv sales_mar.csv \
  -o q1_cleaned.xlsx \
  --date-cols date,created_at \
  --rename "Sale Price:sale_price" \
  --fillna 0 \
  --verbose

🤝 Contributing

Pull requests are welcome!
Feel free to open issues for:

Feature requests

Bug reports

Enhancement ideas

📄 License

This project is open-source under the MIT License.
