import requests
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
# payment and billing endpoints startss

# -------------------------
# payment_url generation
# -------------------------
MERCHANT_ID = ""  # کدی که زرین‌پال بهت میده
CALLBACK_URL = ""         # آدرس برگشت بعد از پرداخت

@payments_router.get("/pay")
def create_payment(amount: int):
    req_data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,  # مبلغ به ریال (اینجا: 2000 تومان)
        "callback_url": CALLBACK_URL,
        "description": "پرداخت تستی برای خدمات سایت"
    }
    headers = {"accept": "application/json",
               "content-type": "application/json"}

    response = requests.post("https://api.zarinpal.com/pg/v4/payment/request.json",
                             json=req_data, headers=headers)
    data = response.json()
    if data["data"]["code"] == 100:
        # هدایت کاربر به درگاه زرین پال
        return {"payment_url": f"https://www.zarinpal.com/pg/StartPay/{data['data']['authority']}"}
    else:
        return {"error": data}


# -------------------------
# verify_payment
# -------------------------
@payments_router.get("/verify")
def verify_payment(request: Request, amount: int):
    authority = request.query_params.get("Authority")
    status = request.query_params.get("Status")

    if status != "OK":
        return {"status": "failed", "message": "پرداخت لغو شد"}

    req_data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,   # باید همون مبلغ مرحله قبل باشه
        "authority": authority
    }
    headers = {"accept": "application/json",
               "content-type": "application/json"}

    response = requests.post("https://api.zarinpal.com/pg/v4/payment/verify.json",
                             json=req_data, headers=headers)
    data = response.json()
    if data["data"]["code"] == 100:
        return {"status": "success", "ref_id": data["data"]["ref_id"]}
    else:
        return {"status": "failed", "error": data}
