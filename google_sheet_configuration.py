import gspread
from oauth2client.service_account import ServiceAccountCredentials
from configure import service_account_info, Config
# setting up google_sheet
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
spreadsheet = client.open(Config.SHEET_NAME)
