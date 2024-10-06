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

1. Create a virtual environment 'python -m venv .venv'
2. Activate the virtual environment (Windows) '.venv\Scripts\activate'
   Activate the virtual environment (Mac/Linux) 'source .venv/bin/activate'
3. Install required dependencies 'pip install pandas requests openpyxl'

# Send Payments Script (`send_payments.py`)

This Python script automates the process of sending payment requests to the DTOne API. It reads payment details from an Excel spreadsheet, sends the payment requests via HTTP POST, and logs the responses in a new Excel file.

## Excel File
The script reads payment details from an Excel file. Update the script to point to the correct file path by modifying this line:

file_path = 'path/to/your/excel/file.xlsx'

The Excel file should have the following columns:

NEW EXTERNAL ID: External ID for each transaction.

PRODUCT ID: The product ID for the payment.

CREDIT PARTY MOBILE NUMBER: The mobile number to which the payment is sent.

Make Payment with Script: A boolean (True/False) column to indicate whether to send payment for that row.

### Logging
A log of the payment transactions is saved as transaction_log.xlsx. It includes the transaction number, mobile number, status, external ID, response ID, and response message.

### How to Run
Ensure your api_credentials.json file, the Excel file with payment data, and the send_payments.py script are in the same directory.

Run the script using Python:

python send_payments.py

The script will:

Load the API credentials from api_credentials.json.
Read payment data from the Excel file.
Send a payment request for each row flagged for payment.
Log the transaction status and responses in a new Excel file (transaction_log.xlsx).

### Output
Console Output: The script will print information about each transaction, indicating whether the payment request was successful or failed.

Excel Log: A file called transaction_log.xlsx will be generated, containing a log of all payment transactions.

### Error Handling
If a payment request fails (e.g., the API returns a non-201 status code), the error message and the status code will be logged in the console and the log file.

### Notes
The script uses HTTP Basic Authentication with credentials stored in api_credentials.json.
It is important to review and update the Excel file before running the script to ensure only intended payments are made.
Be cautious with the auto_confirm parameter in the payload to avoid unintended payments.

### License
This project is licensed under the MIT License.
