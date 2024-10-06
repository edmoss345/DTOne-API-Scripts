import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

# Load API credentials from a separate JSON file
with open('api_credentials.json', 'r') as file:
    credentials = json.load(file)
    API_KEY = credentials['API_KEY']
    API_SECRET = credentials['API_SECRET']

# API live endpoint URL
api_base_url = "https://dvs-api.dtone.com/v1"  

# Read the Excel file and load the transaction IDs into a list
excel_file_path = "transaction_log.xlsx"  # Replace with your file path
df = pd.read_excel(excel_file_path)
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
    url = f"{api_base_url}/transactions/{transaction_id}"
    
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
        mobile_number = transaction_status.get("beneficiary", {}).get("mobile_number")

        print(status_message)

        # Append the result to the list
        results.append({
            "Transaction ID": id,
            "Mobile Number": mobile_numbers[index-1],
            "External ID": external_id,
            "Creation Date": creation_date,
            "Status Message": status_message,
            "Product Name": product_name
        })
    else:
        # Append the failed result to the list
        results.append({
            "Transaction ID": transaction_id,
            "Mobile Number": mobile_numbers[index],
            "External ID": None,
            "Creation Date": None,
            "Status Message": f"Failed to retrieve status. HTTP Status Code: {response.status_code}",
            "Product Name": None
        })

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Save the DataFrame to an Excel file
output_excel_file_path = "transaction_completion_log.xlsx"  # Name of the output Excel file
results_df.to_excel(output_excel_file_path, index=False)

print(f"Results have been saved to {output_excel_file_path}")
