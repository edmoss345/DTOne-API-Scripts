import sys
from os import getenv
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

from dotenv import load_dotenv

load_dotenv(override=True)

DTONE_CREDENTIALS_FILE = getenv("DTONE_CREDENTIALS_FILE")
DTONE_API_URL = getenv("DTONE_API_URL")
TRANSACTIONS_FILE= getenv("TRANSACTIONS_FILE", "transaction_log.xlsx")
COMPLETION_LOG=getenv("COMPLETION_LOG", "transaction_completion_log.xlsx")

# Load API credentials from a separate JSON file
with open(DTONE_CREDENTIALS_FILE, 'r') as file:
    credentials = json.load(file)
    API_KEY = credentials['API_KEY']
    API_SECRET = credentials['API_SECRET']

# Read the Excel file and load the transaction IDs into a list
excel_file_path = TRANSACTIONS_FILE
df = pd.read_excel(excel_file_path, dtype={'Response ID': str})
transaction_ids = df['Response ID'].tolist()
mobile_numbers = df['Mobile Number'].tolist()

# List to store transaction results
results = []

# Get the total number of transaction IDs
total_transactions = len(transaction_ids)

# Iterate through each transaction ID and make API requests
for index, transaction_id in enumerate(transaction_ids, start=1):
    # Print progress message
    print(f"Reviewing record {index} of {total_transactions}")
    
    # Construct the request URL
    url = f"{DTONE_API_URL}/transactions/{transaction_id}"

    # Make the GET request with Basic Auth
    response = requests.get(url, auth=HTTPBasicAuth(API_KEY, API_SECRET))
    
    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        transaction_status = response.json()
        
        # Extract specific items from the JSON response
        id = transaction_status.get("id")
        external_id = transaction_status.get("external_id")
        creation_date = transaction_status.get("creation_date")
        status_message = transaction_status.get("status", {}).get("message")
        product_name = transaction_status.get("product", {}).get("name")
        operator_name = transaction_status.get("product", {}).get("operator").get("name")
        destination = transaction_status.get("requested_values", {}).get("destination",{})
        destination_amount = destination.get("amount", None)
        destination_currency = destination.get("unit", None)
        mobile_number = transaction_status.get("beneficiary", {}).get("mobile_number")

        print(status_message)

        # Append the result to the list
        results.append({
            "Transaction ID": id,
            "Mobile Number": mobile_numbers[index-1],
            "External ID": external_id,
            "Creation Date": creation_date,
            "Status Message": status_message,
            "Product Name": product_name,
            "Operator Name": operator_name,
            "Requested amount": destination_amount,
            "Requested currency": destination_currency
        })
    else:
        # Append the failed result to the list
        results.append({
            "Transaction ID": transaction_id,
            "Mobile Number": mobile_numbers[index-1],
            "External ID": None,
            "Creation Date": None,
            "Status Message": f"Failed to retrieve status. HTTP Status Code: {response.status_code}",
            "Product Name": None,
            "Operator Name": None,
            "Requested amount": None,
            "Requested currency": None
        })

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Save the DataFrame to an Excel file
results_df.to_excel(COMPLETION_LOG, index=False)

print(f"Results have been saved to {COMPLETION_LOG}")
