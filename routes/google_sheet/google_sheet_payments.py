from fastapi import APIRouter, Depends, HTTPException, status, Request
from controllers.google_sheet.google_sheet_payments import PaymentsController
from schema.google_sheet.payments import Payment
from dependencies import AccessTokenBearer

payments_router = APIRouter()
access_token_bearer = AccessTokenBearer()

async def get_current_user(token: str = Depends(access_token_bearer)):
    # TODO: decode token and get user_id
    return 1  # stub user_id

@payments_router.get("/", response_model=list)
async def get_payments(user_id: int = Depends(get_current_user)):
    records = await PaymentsController.get_all_payments()
    return [r for r in records if int(r["user_id"]) == user_id]

@payments_router.get("/admin", response_model=list)
async def admin_list_payments():
    return await PaymentsController.get_all_payments()

@payments_router.post("/")
async def create_payment(payment: Payment):
    return await PaymentsController.create_payment(payment)
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
