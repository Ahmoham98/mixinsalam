from fastapi import APIRouter, Depends, HTTPException, status, Request
from controllers.google_sheet.google_sheet_usage_records import UsageRecordsController
from controllers.google_sheet.google_sheet_users import UsersOperationController
from schema.google_sheet.google_sheet_users import Users
from schema.google_sheet.usage_records import UsageRecord
from dependencies import AccessTokenBearer

usage_router = APIRouter()
access_token_bearer = AccessTokenBearer()

async def get_current_user(token: str = Depends(access_token_bearer)):
    # TODO: decode token and get user_id
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for user in users:
        if user.get("mixin_access_token") == token or user.get("basalam_access_token") == token:
            return user
    raise HTTPException(status_code=401, detail="User not found for provided token")

@usage_router.get("/", response_model=list)
async def get_usage(user: Users = Depends(get_current_user)):
    user_id = user["id"]
    records = await UsageRecordsController.get_all_usage_records()
    return records

@usage_router.post("/increment")
async def increment_usage(record: UsageRecord, user: Users = Depends(get_current_user), request: Request = None):
    usage_type = request.query_params.get("type") if request else None
    # Fetch current usage record
    user_id = user["id"]
    records = await UsageRecordsController.get_all_usage_records()
    usage = next((u for u in records if int(u["user_id"]) == user_id), None)
    if not usage:
        # Create new usage record if not exists
        if usage_type == "migration":
            record.migration_used = 1
            record.realtime_used = 0
        elif usage_type == "realtime":
            record.migration_used = 0
            record.realtime_used = 1
        await UsageRecordsController.create_usage_record(record, user)
        return {"message": "Usage record created"}
    # Increment usage
    if usage_type == "migration":
        usage["migration_used"] = int(usage["migration_used"]) + 1
    elif usage_type == "realtime":
        usage["realtime_used"] = int(usage["realtime_used"]) + 1
    await UsageRecordsController.update_usage_record(int(usage["id"]), UsageRecord(**usage),  user)
    return {"message": "Usage incremented"}

@usage_router.get("/admin", response_model=list)
async def admin_list_usage():
    return await UsageRecordsController.get_all_usage_records()
