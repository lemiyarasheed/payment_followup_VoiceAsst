from flask import Flask, request, jsonify
import pandas as pd
import requests
import os

app = Flask(__name__)

# Load the existing Excel sheet or create a new one
EXCEL_FILE = "customer_responses.xlsx"

# Function to update Excel
def update_excel(data):
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Customer Name", "Invoice Number", "Response", "Last Call Date"])

    # Append new data
    new_entry = pd.DataFrame([data])
    df = pd.concat([df, new_entry], ignore_index=True)
    
    # Save back to Excel
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Receive data from VAPI

    customer_name = data.get("customer_name")
    invoice_number = data.get("invoice_number")
    response = data.get("customer_response")
    
    # Save data to Excel
    update_excel({
        "Customer Name": customer_name,
        "Invoice Number": invoice_number,
        "Response": response,
        "Last Call Date": pd.Timestamp.now()
    })
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


