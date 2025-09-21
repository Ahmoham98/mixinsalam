from routes.google_sheet.google_sheet_users import sheet
# import google sheet from shecma
from schema.google_sheet.google_sheet_users import Users

class UsersOperationController:
    def __init__(self) -> None:
        pass

    async def craete_new_user_in_google_sheet(user: Users):
        sheet.appened_row([Users.mixin_access_token, Users.basalam_access_token, Users.email, Users.created_at, Users.updated_at, Users.is_active, Users.role, Users.is_verified])
        return {"message": "product added successfully"}

    async def get_all_users_from_google_sheet():
        records = sheet.get_all_records()
        return records