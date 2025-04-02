import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Google Sheets Setup
SHEET_ID = "12Tzk2JvZpUy-vc5tic69D4eXzHSMABkVZlQrl8rzuFs"  # Replace with your Google Sheet ID
CREDENTIALS_FILE = "credentials.json"  # Ensure this file is in your project

# Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1  # Access first sheet

# Function to update Google Sheet
def update_google_sheet(data):
    row = [data["Customer Name"], data["Invoice Number"], data["Response"], pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')]
    sheet.append_row(row)  # Append new data to Google Sheet

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Receive data from VAPI

    customer_name = data.get("customer_name")
    invoice_number = data.get("invoice_number")
    response = data.get("customer_response")

    # Save data to Google Sheets
    update_google_sheet({
        "Customer Name": customer_name,
        "Invoice Number": invoice_number,
        "Response": response
    })

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)
