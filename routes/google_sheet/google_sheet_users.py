from fastapi import APIRouter, Depends, Query

from google_sheet_configuration import spreadsheet
# schema importation
from schema.google_sheet.google_sheet_users import Users
# controller importation
from controllers.google_sheet.google_sheet_users import UsersOperationController

from routes.google_sheet.google_sheet_subscriptions import get_current_user

from dependencies import AccessTokenBearer

# imporitng users sheet from googlesheet connection in google_sheet_configuration.py file
sheet = spreadsheet.worksheet("users")

access_token_bearer = AccessTokenBearer()



users_google_sheet = APIRouter()

# pydantic mdoel needed

@users_google_sheet.post("/user/")
async def create_new_user(
    user: Users,
    token: str = Depends(access_token_bearer)
):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for idx, u in enumerate(users, start=2):  # start=2 to match Google Sheet row numbers
        if u.get("mixin_access_token") == user.mixin_access_token or u.get("basalam_access_token") == user.basalam_access_token:
            from routes.google_sheet.google_sheet_users import sheet
            sheet.update_cell(idx, 2, user.mixin_access_token)  # Column 2: mixin_access_token
            sheet.update_cell(idx, 3, user.basalam_access_token)  # Column 3: basalam_access_token
            return {"message": "User tokens updated"}
    result = await UsersOperationController.craete_new_user_in_google_sheet(user)
    return {"message": f"User is successfully created! {result}"}


@users_google_sheet.put("/user/email")
async def update_user_email(
    email: str = Query(..., description="New email for the user"),
    user=Depends(get_current_user)
):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for idx, u in enumerate(users, start=2):
        if u.get("mixin_access_token") == user["mixin_access_token"] or u.get("basalam_access_token") == user["basalam_access_token"]:
            from routes.google_sheet.google_sheet_users import sheet
            sheet.update_cell(idx, 4, email)  # Column 4: email
            return {"message": "User email updated"}
    return {"message": "User not found"}

@users_google_sheet.get("/user/")
async def get_all_users(
    token: str = Depends(access_token_bearer)
):
    result = await UsersOperationController.get_all_users_from_google_sheet()
    return {
        "message": "successs", 
        "response": f"{result}"
    }