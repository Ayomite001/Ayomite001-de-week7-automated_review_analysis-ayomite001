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



def staging(client = gspread.authorize(cred), sheet_id = "11JDDG8EdE5aVMQHZmFYIVspP7Epo9tAeFcId13HZPB0"):

    workbook = client.open_by_key(sheet_id)
    raw_sheet = workbook.worksheet("raw_data")

    raw_data = raw_sheet.get_all_records()
    df = pd.DataFrame(raw_data)


    df.dropna(how="all", inplace=True)

    # strip spaces & lowercase
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.lower()

    try:
        staging_sheet = workbook.worksheet("staging")
        staging_sheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        staging_sheet = workbook.add_worksheet(
            title="staging",
            rows=len(df) + 5,
            cols=len(df.columns) + 5
        )

    # 5. Upload cleaned data
    staging_sheet.update(
        [df.columns.tolist()] + df.values.tolist()
    )

    print("Staging worksheet created and cleaned data loaded successfully.")



def processed(client = gspread.authorize(cred), sheet_id = "11JDDG8EdE5aVMQHZmFYIVspP7Epo9tAeFcId13HZPB0"):

    workbook = client.open_by_key(sheet_id)

    raw_sheet = workbook.worksheet("staging")

    staging = raw_sheet.get_all_records()
    df  = pd.DataFrame(staging)

    df["AI Sentiment"] = ""
    df["AI Summary"] = ""
    df["Action Needed"] = ""


    try:
        processed_sheet = workbook.worksheet("processed")
        processed_sheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        processed_sheet = workbook.add_worksheet(
            title="processed",
            rows=len(df) + 5,
            cols=len(df.columns) + 5
        )

    # Upload dataframe to processed sheet
    processed_sheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("Processed sheet created successfully!")
    return processed_sheet

    

staging()
processed()










