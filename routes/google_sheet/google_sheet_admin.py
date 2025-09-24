from fastapi import APIRouter, Depends, HTTPException
from controllers.google_sheet.google_sheet_users import UsersOperationController
from controllers.google_sheet.google_sheet_plans import PlansController
from controllers.google_sheet.google_sheet_subscription import SubscriptionsController
from controllers.google_sheet.google_sheet_usage_records import UsageRecordsController
from controllers.google_sheet.google_sheet_payments import PaymentsController
from dependencies import AccessTokenBearer

admin_router = APIRouter()
access_token_bearer = AccessTokenBearer()

async def is_admin(token: str = Depends(access_token_bearer)):
    # TODO: decode token and check user role
    return True

@admin_router.get("/api/admin/users", dependencies=[Depends(is_admin)])
async def list_users():
    return await UsersOperationController.get_all_users_from_google_sheet()

@admin_router.get("/api/admin/plans", dependencies=[Depends(is_admin)])
async def list_plans():
    return await PlansController.get_all_plans()

@admin_router.get("/api/admin/subscriptions", dependencies=[Depends(is_admin)])
async def list_subscriptions():
    return await SubscriptionsController.get_all_subscriptions()

@admin_router.get("/api/admin/usage", dependencies=[Depends(is_admin)])
async def list_usage():
    return await UsageRecordsController.get_all_usage_records()

@admin_router.get("/api/admin/payments", dependencies=[Depends(is_admin)])
async def list_payments():
    return await PaymentsController.get_all_payments()
