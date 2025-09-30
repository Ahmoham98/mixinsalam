import gspread
from oauth2client.service_account import ServiceAccountCredentials
from configure import service_account_info, Config
# setting up google_sheet
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

from google.auth import jwt
from google.auth.transport.requests import Request
import datetime

# Load credentials (assuming service account JSON)
from google.oauth2 import service_account
creds = service_account.Credentials.from_service_account_file(
    "service-account.json",  # adjust path
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Build a JWT manually to inspect claims
signer = creds.signer
info = creds.service_account_email

now = int(datetime.datetime.utcnow().timestamp())
payload = {
    "iss": info,
    "scope": "https://www.googleapis.com/auth/spreadsheets",
    "aud": "https://oauth2.googleapis.com/token",
    "iat": now,
    "exp": now + 3600,  # must be within 1 hour
}

print("JWT debug:", payload)


spreadsheet = client.open(Config.SHEET_NAME)
