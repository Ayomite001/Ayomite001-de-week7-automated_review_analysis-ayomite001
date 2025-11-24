import gspread
import numpy as np
import pandas as pd
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

cred = Credentials.from_service_account_file("credential.json", scopes = scopes)
client = gspread.authorize(cred)

sheet_id = "11JDDG8EdE5aVMQHZmFYIVspP7Epo9tAeFcId13HZPB0"

workbook = client.open_by_key(sheet_id)


# Load dataset
df = pd.read_csv(r"C:\Users\USER\Downloads\Womens Clothing E-Commerce Reviews.csv\Womens Clothing E-Commerce Reviews.csv")

# Take first 200 rows
df = df.head(200)
df = df.replace([np.nan, np.inf, -np.inf], "")

# Check if 'raw_data' exists
try:
    raw_sheet = workbook.worksheet("raw_data")
    raw_sheet.clear()  # Clear existing data
except gspread.exceptions.WorksheetNotFound:
    raw_sheet = workbook.add_worksheet(
        title="raw_data",
        rows=len(df)+5,
        cols=len(df.columns)+5
    )

# Upload header + rows
raw_sheet.update([df.columns.values.tolist()] + df.values.tolist())





