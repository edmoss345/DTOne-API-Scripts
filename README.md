# DTOne API Scripts
This repo has a number of scripts that can be used to make or query transactions using the DTOne API. 

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.x** installed on your system.
2. Required Python libraries: `pandas`, `requests`, `openpyxl`.
3. A JSON file containing your API credentials named `api_credentials.json`. The file should be structured as follows:
   ```json
   {
       "API_KEY": "your_api_key",
       "API_SECRET": "your_api_secret"
   }

It is recommended to run the script within a Python virtual environment to manage dependencies. To set up and activate a virtual environment:

1. Create a virtual environment `python -m venv .venv`
2. Activate the environment:
    - Linux: `source .venv/bin/activate`
    - Windows: `.venv/Scripts/activate`
3. Install required dependencies `pip install pandas requests openpyxl`

# Send Payments Script (`send_payments.py`)
This Python script automates the process of sending payment requests to the DTOne API. It reads payment details from an Excel spreadsheet, sends the payment requests via HTTP POST, and logs the responses in a new Excel file.

## Excel File
The script reads payment details from an Excel file. Update the script to point to the correct file path by modifying this line:

file_path = 'path/to/your/excel/file.xlsx'

The Excel file should have the following columns:
- NEW EXTERNAL ID: External ID for each transaction.
- PRODUCT ID: The product ID for the payment.
- CREDIT PARTY MOBILE NUMBER: The mobile number to which the payment is sent.
- Make Payment with Script: A boolean (True/False) column to indicate whether to send payment for that row.

### Logging
A log of the payment transactions is saved as transaction_log.xlsx. It includes the transaction number, mobile number, status, external ID, response ID, and response message.

### How to Run
Ensure your api_credentials.json file, the Excel file with payment data, and the send_payments.py script are in the same directory.

Run the script using Python:

`python send_payments.py`

The script will:
- Load the API credentials from api_credentials.json.
- Read payment data from the Excel file.
- Send a payment request for each row flagged for payment.
- Log the transaction status and responses in a new Excel file (transaction_log.xlsx).

### Output
Console Output: The script will print information about each transaction, indicating whether the payment request was successful or failed.

Excel Log: A file called transaction_log.xlsx will be generated, containing a log of all payment transactions. This is also the default file path used by the 'transaction lookup' script (see below). So that script can be run immediately after to check the status of all transactions.

### Error Handling
If a payment request fails (e.g., the API returns a non-201 status code), the error message and the status code will be logged in the console and the log file.

### Notes
The script uses HTTP Basic Authentication with credentials stored in api_credentials.json.
It is important to review and update the Excel file before running the script to ensure only intended payments are made.

# Lookup Transactions Script (`bulk_lookup_transaction.py`)
This Python script retrieves the status of previously initiated transactions from the DTOne API. It reads transaction IDs from an Excel file, makes API requests to retrieve the current status of each transaction, and logs the results in a new Excel file.

## Excel File
The script reads transaction IDs and mobile numbers from an Excel file (transaction_log.xlsx). Update the script to point to the correct file path by modifying this line:

excel_file_path = "path/to/your/excel/transaction_log.xlsx"

The Excel file should contain the following columns:
- Response ID: The transaction ID used to query the status.
- Mobile Number: The mobile number associated with the transaction.

## Output
The results of the status review will be saved in a new Excel file, transaction_completion_log.xlsx, containing the following columns:
- Transaction ID: The transaction ID queried from the API.
- Mobile Number: The associated mobile number from the original Excel file.
- External ID: The external ID of the transaction (if available).
- Creation Date: The date the transaction was created.
- Status Message: The current status message of the transaction.
- Product Name: The name of the product associated with the transaction.

Console Output: The script will print progress and status messages for each transaction, indicating whether the status was successfully retrieved or if the request failed.

## How to Run
Ensure your api_credentials.json file and the Excel file with transaction data are in the same directory as the script.

Run the script using Python:

`python review_transactions.py`

The script will:

- Load the API credentials from api_credentials.json.
- Read the transaction IDs and mobile numbers from the Excel file.
- Query the DTOne API for each transaction’s status.
- Save the results in a new Excel file (transaction_completion_log.xlsx).
