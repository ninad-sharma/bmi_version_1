# sheets.py — Safe Google Sheets connector using .env + gspread

import os
import gspread
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Load .env (must exist in your Project Folder)
load_dotenv()

# Get path to service account file
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not SERVICE_ACCOUNT_FILE or not Path(SERVICE_ACCOUNT_FILE).exists():
    raise FileNotFoundError(
        f"Service account file not found. "
        f"Expected at {SERVICE_ACCOUNT_FILE}. "
        f"Check your .env setup."
    )

# Connect to Google Sheets with gspread
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)

# Your spreadsheet ID (from the URL)
SPREADSHEET_ID = "1BgVkSsGTMJB3_NKiKtoicpg83g4jS4aI-wLPN0J27q8"


def read_sheet(tab_name: str) -> pd.DataFrame:
    """
    Read a tab from the spreadsheet into a Pandas DataFrame.
    """
    sh = gc.open_by_key(SPREADSHEET_ID)
    ws = sh.worksheet(tab_name)
    records = ws.get_all_records()
    return pd.DataFrame(records)


if __name__ == "__main__":
    TAB_NAME = "players"  # exact tab name

    print(f"Reading tab: {TAB_NAME}")
    df = read_sheet(TAB_NAME)
    print(f"Rows read: {len(df)}")

    if not df.empty:
        print("First row:", df.iloc[0].to_dict())
    else:
        print("No data found in this tab.")

    # Always save CSV
    os.makedirs("data", exist_ok=True)
    out_path = os.path.abspath(os.path.join("data", f"{TAB_NAME}.csv"))
    df.to_csv(out_path, index=False)
    print(f"Saved to: {out_path}")
