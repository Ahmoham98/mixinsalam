from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_305_USE_PROXY
from controllers.google_sheet.google_sheet_plans import PlansController
from controllers.google_sheet.google_sheet_users import UsersOperationController
from schema.google_sheet.plans import Plan
from dependencies import AccessTokenBearer

plans_router = APIRouter()
access_token_bearer = AccessTokenBearer()

# Helper: check admin (stub, replace with real logic)
async def is_admin(token: str = Depends(access_token_bearer)):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for user in users:
        if user.get("mixin_access_token") == token or user.get("basalam_access_token") == token:
            if user["role"] == "admin":
                return True
            else:
                raise HTTPException(status_code=403, detail="you don't have enough privilages!")
        raise HTTPException(status_code=401, detail="User not found for provided token")

@plans_router.get("/", response_model=list)
async def list_plans():
    return await PlansController.get_all_plans()

@plans_router.get("/{plan_id}")
async def get_plan(plan_id: int):
    plan = await PlansController.get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@plans_router.post("/", dependencies=[Depends(is_admin)])
async def create_plan(plan: Plan):
    return await PlansController.create_plan(plan)

@plans_router.put("/{plan_id}", dependencies=[Depends(is_admin)])
async def update_plan(plan_id: int, plan: Plan):
    return await PlansController.update_plan(plan_id, plan)

@plans_router.delete("/{plan_id}", dependencies=[Depends(is_admin)])
async def delete_plan(plan_id: int):
    return await PlansController.delete_plan(plan_id)
