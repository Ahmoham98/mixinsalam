from fastapi import FastAPI
from fastapi.requests import Request
import logging
import time

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from controllers.google_sheet.google_sheet_usage_records import UsageRecordsController
from controllers.google_sheet.google_sheet_subscription import SubscriptionsController
from controllers.google_sheet.google_sheet_plans import PlansController
from controllers.google_sheet.google_sheet_users import UsersOperationController


logger = logging.getLogger('uvicorn.access')
logger.disabled = True

async def get_user_by_token(token: str):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for user in users:
        if user.get("mixin_access_token") == token or user.get("basalam_access_token"):
            return user
    else:
        return None


def register_middleware(app: FastAPI):
    
    
    origins = [
        "http://localhost:5173",
        "http://myapp.test:5173",
        "https://mixinsalamm.liara.run",  # Frontend URL
        "https://mixinsalam.liara.run",   # Backend URL
        "http://localhost:3000",
        "https://mixinsalama-reactt.liara.run",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials= True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = ["*"]
    )
    
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        processing_time = time.time() - start_time
        
        message = f" {request.client.host} - {request.client.port} - {request.method} - {request.url.path} - {request.state} - completed after: -- {processing_time} -- "
        print(message)
        
        return response 

class QuotaEnforcementMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # skip option requests
        if request.method == "OPTIONS":
            return await call_next(request)
        # Only enforce on relevant endpoints
        if request.url.path.startswith("/api/usage/increment") or \
           request.url.path.startswith("/api/products/migrate") or \
           request.url.path.startswith("/api/products/realtime-update"):
            # Extract token
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})
            
            token = auth.split(" ", 1)[1]
            user = await get_user_by_token(token)
            user_id = user["id"]
            # Get current subscription
            subs = await SubscriptionsController.get_all_subscriptions()
            sub = next((s for s in subs if int(s["user_id"]) == user_id and s["status"] == "active"), None)
            if not sub:
                return JSONResponse(status_code=402, content={"detail": "No active subscription. Payment required."})
            plan_id = int(sub["plan_id"])
            plan = await PlansController.get_plan_by_id(plan_id)
            if not plan:
                return JSONResponse(status_code=500, content={"detail": "Plan not found"})
            # Get usage
            usage_records = await UsageRecordsController.get_all_usage_records()
            usage = next((u for u in usage_records if int(u["user_id"]) == user_id), None)
            migration_used = int(usage["migration_used"]) if usage else 0
            realtime_used = int(usage["realtime_used"]) if usage else 0
            # Enforce quotas
            if request.url.path.endswith("migrate") and migration_used >= int(plan["quota_migration"]):
                return JSONResponse(status_code=429, content={"detail": "Migration quota exceeded"})
            if request.url.path.endswith("realtime-update") and realtime_used >= int(plan["quota_realtime_updates"]):
                return JSONResponse(status_code=429, content={"detail": "Real-time update quota exceeded"})
        response = await call_next(request)
        return response 
