import requests
from requests.auth import HTTPBasicAuth
import json

# Load API credentials from a separate JSON file
with open('api_credentials.json', 'r') as file:
    credentials = json.load(file)
    API_KEY = credentials['API_KEY']
    API_SECRET = credentials['API_SECRET']

# API live endpoint URL
api_base_url = "https://dvs-api.dtone.com/v1"  

transaction_id = "7461865111"

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

    # Print the extracted items
    print("Transaction ID:", id)
    print("External ID:", external_id)
    print("Creation Date:", creation_date)
    print("Status Message:", status_message)
    print("Product Name:", product_name)
else:
    print("Failed to retrieve transaction status. HTTP Status Code:", response.status_code)
    print("Response:", response.text)
