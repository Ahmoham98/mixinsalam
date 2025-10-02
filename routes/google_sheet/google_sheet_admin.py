from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import false
from sqlalchemy.sql import true
from controllers.google_sheet.google_sheet_users import UsersOperationController
from controllers.google_sheet.google_sheet_plans import PlansController
from controllers.google_sheet.google_sheet_subscription import SubscriptionsController
from controllers.google_sheet.google_sheet_usage_records import UsageRecordsController
from controllers.google_sheet.google_sheet_payments import PaymentsController
from dependencies import AccessTokenBearer
from routes.google_sheet.google_sheet_subscriptions import get_current_user
from schema.google_sheet.google_sheet_users import Users

admin_router = APIRouter()
access_token_bearer = AccessTokenBearer()

async def is_admin(token: str = Depends(access_token_bearer)):
    # TODO: decode token and check user role
    user = await get_current_user(token)
    #checkes admin privilage
    if user["role"] == "admin":
        return True
    else:
        return False

@admin_router.get("/api/admin/users")
async def list_users(check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await UsersOperationController.get_all_users_from_google_sheet()
    else:
        return "you don't have enough privilages"

@admin_router.get("/api/admin/plans")
async def list_plans(check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await PlansController.get_all_plans()
    else:
        return "you don't have enough privilages"
    

@admin_router.get("/api/admin/subscriptions")
async def list_subscriptions(check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await SubscriptionsController.get_all_subscriptions()
    else:
        return "you don't have enough privilages"

@admin_router.get("/api/admin/usage")
async def list_usage(check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await UsageRecordsController.get_all_usage_records()
    else:
        return "you don't have enough privilages"
    

@admin_router.get("/api/admin/payments")
async def list_payments(check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await PaymentsController.get_all_payments()
    else:
        return "you don't have enough privilages"
    
