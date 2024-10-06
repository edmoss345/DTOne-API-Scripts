import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from openpyxl import Workbook
import json

# Load API credentials from a separate JSON file
with open('api_credentials.json', 'r') as file:
    credentials = json.load(file)
    API_KEY = credentials['API_KEY']
    API_SECRET = credentials['API_SECRET']

# API live endpoint URL
url = "https://dvs-api.dtone.com/v1/async/transactions"  

# Load the data from the Excel spreadsheet
file_path = 'C:/Users/edmun/OneDrive - EEM Engineering Ltd/IDEMS/RCT/1 Month Payments.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(file_path, sheet_name='Tel Number Payments to Make')

# Create a new Excel workbook for logging
log_wb = Workbook()
log_ws = log_wb.active
log_ws.title = "Transaction Log"

# Write headers to the log file
log_ws.append(["Transaction Number", "Mobile Number", "Status", "External ID", "Response ID", "Response Message"])

# Iterate through each row in the dataframe and send the API request
for index, row in df.iterrows():
    # Extract values from the row using the correct column names
    external_id = row['NEW EXTERNAL ID']
    product_id = row['PRODUCT ID']
    mobile_number = '+'+ str(row['CREDIT PARTY MOBILE NUMBER'])
    make_payment = row['Make Payment with Script']

    if make_payment:

        # Prepare the payload data
        payload = {
            "external_id": external_id,
            "product_id": product_id,
            "credit_party_identifier": {
                "mobile_number": mobile_number
            },
            "auto_confirm": True
        }

        # Making the POST request with HTTP Basic Authentication
        print(f"Processsing: number: {mobile_number}, external_id:{external_id}, product_id:{product_id}")
        response = requests.post(url, json=payload, auth=HTTPBasicAuth(API_KEY, API_SECRET))

        # Check the response status
        if response.status_code == 201:
            status = "Success"
            response_message = response.json()
            print(f"Payment request sent successfully for {external_id}, phone number {mobile_number}. Responde ID: {response_message['id']}")
        else:
            status = "Failed"
            print(response.text)
            response_message = response.text
            print(f"Failed to send payment request for {external_id}: {response.status_code}, phone number {mobile_number}")
            
        # Append the transaction log to the Excel sheet
        log_ws.append([index + 1, mobile_number, status, external_id, response_message['id'], str(response_message)])

    else:
        print(f"Skipping number: {mobile_number}, not flagged for payment in excel")


# Save the log file
log_file_path = 'transaction_log.xlsx'  # Define the path where you want to save the log
log_wb.save(log_file_path)
print(f"Transaction log saved to {log_file_path}")