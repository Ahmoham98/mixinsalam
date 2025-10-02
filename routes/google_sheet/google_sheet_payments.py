from ast import Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from controllers.google_sheet.google_sheet_payments import PaymentsController
from schema.google_sheet.google_sheet_users import Users
from controllers.google_sheet.google_sheet_users import UsersOperationController
from schema.google_sheet.payments import Payment
from dependencies import AccessTokenBearer

payments_router = APIRouter()
access_token_bearer = AccessTokenBearer()

async def get_current_user(token: str = Depends(access_token_bearer)):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for user in users:
        if user.get("mixin_access_token") == token or user.get("basalam_access_token") == token:
            return user
    raise HTTPException(status_code=401, detail="User not found for provided token")

@payments_router.get("/")
async def get_payments(user: Users = Depends(get_current_user)):
    user_id = user["id"]
    records = await PaymentsController.get_all_payments()
    return [r for r in records if int(r["user_id"]) == user_id]

@payments_router.get("/admin", response_model=list)
async def admin_list_payments():
    return await PaymentsController.get_all_payments()

@payments_router.post("/")
async def create_payment(payment: Payment, user: Users = Depends(get_current_user)):
    return await PaymentsController.create_payment(payment, user)
# payment and billing endpoints starts
@payments_router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    # TODO: Parse and verify Stripe event, update payment/subscription status in Google Sheet
    # This is a stub for now
    return {"message": "Webhook received"}

@payments_router.get("/{payment_id}/invoice")
async def download_invoice(payment_id: int):
    payment = await PaymentsController.get_payment_by_id(payment_id)
    if not payment or not payment.get("invoice_url"):
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"invoice_url": payment["invoice_url"]}
