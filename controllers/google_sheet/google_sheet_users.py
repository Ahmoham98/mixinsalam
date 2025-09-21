# import google sheet from shecma
from schema.google_sheet.google_sheet_users import Users

class UsersOperationController:
    def __init__(self) -> None:
        pass

    async def craete_new_user_in_google_sheet(user: Users):
        from routes.google_sheet.google_sheet_users import sheet
        sheet.append_row([user.mixin_access_token, user.basalam_access_token, user.email, user.created_at, user.updated_at, user.is_active, user.role, user.is_verified])
        return {"message": "product added successfully"}

    async def get_all_users_from_google_sheet():
        from routes.google_sheet.google_sheet_users import sheet
        records = sheet.get_all_records()
        return records