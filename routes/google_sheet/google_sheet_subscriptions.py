from fastapi import APIRouter, Depends, HTTPException, status
from controllers.google_sheet.google_sheet_subscription import SubscriptionsController
from schema.google_sheet.subscriptions import Subscription
from schema.google_sheet.google_sheet_users import Users
from dependencies import AccessTokenBearer
from controllers.google_sheet.google_sheet_users import UsersOperationController

subscriptions_router = APIRouter()
access_token_bearer = AccessTokenBearer()

# gets current user base on the access token in the header which can be from mixin or basalam
async def get_current_user(token: str = Depends(access_token_bearer)):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for user in users:
        if user.get("mixin_access_token") == token or user.get("basalam_access_token") == token:
            return user
    raise HTTPException(status_code=401, detail="User not found for provided token")

@subscriptions_router.get("/", response_model=list)
async def list_subscriptions(user: Users = Depends(get_current_user)):
    # Admin: list all, user: list own
    # TODO: check admin
    if user.role == "admin":
        return await SubscriptionsController.get_all_subscriptions()

@subscriptions_router.get("/current")
async def get_current_subscription(user: Users = Depends(get_current_user)):
    user_id = user["id"]
    subs = await SubscriptionsController.get_all_subscriptions()
    for sub in subs:
        
        if sub["user_id"] == user_id and sub["status"] == "active":
            return sub
    raise HTTPException(status_code=404, detail="No active subscription")

@subscriptions_router.post("/")
async def subscribe(sub: Subscription, user: Users =Depends(get_current_user)):
    # TODO: check plan validity, payment, etc.
    return await SubscriptionsController.create_subscription(sub, user)

@subscriptions_router.put("/{sub_id}")
async def update_subscription(sub_id: int, sub: Subscription, user=Depends(get_current_user)):
    return await SubscriptionsController.update_subscription(sub_id, sub, user)

@subscriptions_router.delete("/{sub_id}")
async def cancel_subscription(sub_id: int, user=Depends(get_current_user)):
    return await SubscriptionsController.delete_subscription(sub_id)
