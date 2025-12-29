# DTOne API Scripts

This repository contains Python scripts for **sending payments** and **querying transaction status** using the DTOne API. The scripts are designed to work together using Excel files for input and output, and environment variables for configuration.

---

## Prerequisites

Before running the scripts, ensure you have:

1. **Python 3.9+** installed
2. All required Python libraries listed in `requirements.txt`
3. One or more DTOne API credential JSON files (for test and/or production)
4. A `.env` file for configuration (see below)

It is recommended to run the scripts inside a Python virtual environment.

### Virtual environment setup

```bash
python -m venv .venv
```

Activate the environment:
- **Linux / macOS**: `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration (`.env` file)

All runtime configuration is handled via environment variables loaded from a `.env` file. Copy `dotenv_example` to `.env` and update as needed.

### Example `.env`

```env
# DTOne API base URL (test or production)
DTONE_API_URL=https://preprod-dvs-api.dtone.com/v1

# Path to API credentials file (JSON)
DTONE_CREDENTIALS_FILE=api_credentials_test.json

# Excel input / output files
PAYMENTS_FILE=Example payments.xlsx
TRANSACTIONS_FILE=transaction_log.xlsx
COMPLETION_LOG=transaction_completion_log.xlsx
```

> **Note:** The scripts use `load_dotenv(override=True)`, so values in `.env` will override any system environment variables.

---

## API Credentials File

The credentials file referenced by `DTONE_CREDENTIALS_FILE` must be a JSON file with the following structure:

```json
{
  "API_KEY": "your_api_key",
  "API_SECRET": "your_api_secret"
}
```

Keep credential files out of version control.

---

## Send Payments Script (`send_payments.py`)

### Purpose

This script sends asynchronous payment requests to the DTOne API based on data in an Excel spreadsheet, and logs the API responses to a transaction log file.

### Input Excel File

The Excel file specified by `PAYMENTS_FILE` must contain a sheet named **`Payments to Make`** with the following columns:

- **NEW EXTERNAL ID** – External reference for the transaction
- **PRODUCT ID** – DTOne product ID
- **CREDIT PARTY MOBILE NUMBER** – Mobile number to credit (without `+`)
- **Make Payment with Script** – Boolean flag (TRUE/FALSE)

Only rows where **Make Payment with Script** is `TRUE` will be processed.

### Output

- An Excel file defined by `TRANSACTIONS_FILE` (default: `transaction_log.xlsx`)
- The log includes:
  - Transaction number
  - Mobile number
  - Status (Success / Failed)
  - External ID
  - Response ID
  - Response message

This file is used as input for the lookup script.

### How to Run

```bash
python send_payments.py
```

### Notes

- Uses HTTP Basic Authentication
- Payments are submitted asynchronously
- Always review the Excel file before running to avoid unintended payments

---

## Lookup Transactions Script (`bulk_lookup_transaction.py`)

### Purpose

This script queries the DTOne API for the status of previously submitted transactions and produces a completion report.

### Input Excel File

By default, the script reads from the file defined by `TRANSACTIONS_FILE` (usually `transaction_log.xlsx`).

The file must contain the following columns:

- **Response ID** – Transaction ID returned by DTOne
- **Mobile Number** – Associated mobile number

### Output

An Excel file defined by `COMPLETION_LOG` (default: `transaction_completion_log.xlsx`) containing:

- Transaction ID
- Mobile Number
- External ID
- Creation Date
- Status Message
- Product Name
- Operator Name
- Requested amount
- Requested currency

### How to Run

```bash
python bulk_lookup_transaction.py
```

### Console Output

The script prints progress information for each transaction and indicates whether the lookup succeeded or failed.

---

## Typical Workflow

1. Configure `.env` and credentials
2. Prepare the payments Excel file
3. Run `send_payments.py`
4. Wait for DTOne to process transactions
5. Run `bulk_lookup_transaction.py`
6. Review the completion log

---

## Troubleshooting

- **Wrong environment used**: Verify `DTONE_API_URL` in `.env`
- **Authentication errors**: Ensure credentials match the selected environment
- **Excel errors**: Confirm file paths, sheet names, and column headers

---

## License

Internal / private use only

