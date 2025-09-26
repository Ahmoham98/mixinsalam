from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routes import basalam_client, google_sheet, mixin_client, product_images, user_products
from routes.google_sheet import google_sheet_users
from routes.google_sheet.google_sheet_plans import plans_router
from routes.google_sheet.google_sheet_subscriptions import subscriptions_router
from routes.google_sheet.google_sheet_usage_records import usage_router
from routes.google_sheet.google_sheet_payments import payments_router
from routes.google_sheet.google_sheet_admin import admin_router
import uvicorn
from middleware import QuotaEnforcementMiddleware

app = FastAPI()

#some comment
origins = [
    "http://localhost:5173",
    "http://myapp.test:5173"
    "https://mixinsalamm.liara.run",  # Frontend URL
    "https://mixinsalam.liara.run",   # Backend URL
    "http://localhost:3000",
    "https://mixinsalama-reactt.liara.run",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials"
    ],
    expose_headers=["Content-Length", "X-Requested-With"],
    max_age=3600,
)

app.add_middleware(QuotaEnforcementMiddleware)

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": origins,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Content-Type, Accept, Authorization, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        }
    )


app.include_router(basalam_client.basalam_client, prefix="/basalam/client", tags=["basalam_client"])
app.include_router(mixin_client.mixin_client, prefix="/mixin/client", tags=["mixin_client"])
app.include_router(user_products.product_router, prefix="/products", tags=["products"])
app.include_router(product_images.image_router, prefix="/images", tags=["product images"])
app.include_router(google_sheet_users.users_google_sheet, prefix="/googlesheet", tags=["google-sheet"])
app.include_router(plans_router, prefix="/api/plans", tags=["plans"])
app.include_router(subscriptions_router, prefix="/api/subscription", tags=["subscription"])
app.include_router(usage_router, prefix="/api/usage", tags=["usage"])
app.include_router(payments_router, prefix="/api/payments", tags=["payments"])
app.include_router(admin_router)


@app.get("/")
async def get_root():
    return "You are very welcome !!!!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=False)

