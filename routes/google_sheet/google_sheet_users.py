from fastapi import APIRouter, Depends

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from configure import Config, service_account_info
# schema importation
from schema.google_sheet.google_sheet_users import Users
# controller importation
from controllers.google_sheet.google_sheet_users import UsersOperationController

from dependencies import AccessTokenBearer





# setting up google sheet
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open(Config.SHEET_NAME).worksheet("users")

access_token_bearer = AccessTokenBearer()



users_google_sheet = APIRouter()

# pydantic mdoel needed

users_google_sheet.post("/user/")
async def create_new_user(
    user: Users,
    token: str = Depends(access_token_bearer)
):
    result = await UsersOperationController.craete_new_user_in_google_sheet(user)
    return f"user is successfully created! {result}"

users_google_sheet.get("/user/")
async def get_all_users(
    token: str = Depends(access_token_bearer)
):
    result = await UsersOperationController.get_all_users_from_google_sheet()
    return {
        "message": "successs", 
        "response": f"{result}"
    }