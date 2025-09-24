from schema.google_sheet.plans import Plan
from google_sheet_configuration import spreadsheet

from utils import utilities

class PlansController:
    sheet = spreadsheet.worksheet("plans")

    @staticmethod
    async def get_all_plans():
        records = PlansController.sheet.get_all_records()
        return records

    @staticmethod
    async def get_plan_by_id(plan_id: int):
        records = PlansController.sheet.get_all_records()
        for record in records:
            if int(record["id"]) == plan_id:
                return record
        return None

    @staticmethod
    async def create_plan(plan: Plan):
        sheet = PlansController.sheet
        next_id = await utilities.get_next_id(sheet)
        PlansController.sheet.append_row([
            next_id, plan.name, plan.price_monthly, plan.quota_migration, plan.quota_realtime_updates,
            plan.is_active, plan.created_at, plan.updated_at
        ])
        return {"message": "Plan created successfully"}

    @staticmethod
    async def update_plan(plan_id: int, plan: Plan):
        records = PlansController.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):  # 2 because header is row 1
            if int(record["id"]) == plan_id:
                PlansController.sheet.update(f"A{idx}:H{idx}", [[
                    plan_id, plan.name, plan.price_monthly, plan.quota_migration, plan.quota_realtime_updates,
                    plan.is_active, plan.created_at, plan.updated_at
                ]])
                return {"message": "Plan updated successfully"}
        return {"error": "Plan not found"}

    @staticmethod
    async def delete_plan(plan_id: int):
        records = PlansController.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == plan_id:
                PlansController.sheet.delete_rows(idx)
                return {"message": "Plan deleted successfully"}
        return {"error": "Plan not found"}
