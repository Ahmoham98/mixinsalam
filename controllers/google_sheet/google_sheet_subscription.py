from schema.google_sheet.subscriptions import Subscription
from google_sheet_configuration import spreadsheet

from utils import utilities

class SubscriptionsController:
    sheet = spreadsheet.worksheet("subscriptions")

    @staticmethod
    async def get_all_subscriptions():
        records = SubscriptionsController.sheet.get_all_records()
        return records

    @staticmethod
    async def get_subscription_by_id(sub_id: int):
        records = SubscriptionsController.sheet.get_all_records()
        for record in records:
            if int(record["id"]) == sub_id:
                return record
        return None

    @staticmethod
    async def create_subscription(sub: Subscription, user):
        sheet = SubscriptionsController.sheet
        next_id = await utilities.get_next_id(sheet)
        user_id = user["id"]
        SubscriptionsController.sheet.append_row([
            next_id, user_id, sub.plan_id, sub.status, sub.start_date, sub.end_date, sub.renewal_date,
            sub.cancel_at_period_end, sub.created_at, sub.updated_at
        ])
        return {"message": "Subscription created successfully"}

    @staticmethod
    async def update_subscription(sub_id: int, sub: Subscription, user):
        records = SubscriptionsController.sheet.get_all_records()
        user_id = user["id"]
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == sub_id:
                SubscriptionsController.sheet.update(f"A{idx}:J{idx}", [[
                    sub_id, user_id, sub.plan_id, sub.status, sub.start_date, sub.end_date, sub.renewal_date,
                    sub.cancel_at_period_end, sub.created_at, sub.updated_at
                ]])
                return {"message": "Subscription updated successfully"}
        return {"error": "Subscription not found"}

    @staticmethod
    async def delete_subscription(sub_id: int):
        records = SubscriptionsController.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == sub_id:
                SubscriptionsController.sheet.delete_rows(idx)
                return {"message": "Subscription deleted successfully"}
        return {"error": "Subscription not found"}
