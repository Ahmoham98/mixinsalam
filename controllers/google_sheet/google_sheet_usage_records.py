from schema.google_sheet.usage_records import UsageRecord
from google_sheet_configuration import spreadsheet
from schema.google_sheet.google_sheet_users import Users
from utils import utilities

class UsageRecordsController:
    sheet = spreadsheet.worksheet("usage_records")

    @staticmethod
    async def get_all_usage_records():
        records = UsageRecordsController.sheet.get_all_records()
        return records

    @staticmethod
    async def get_usage_record_by_id(record_id: int):
        records = UsageRecordsController.sheet.get_all_records()
        for record in records:
            if int(record["id"]) == record_id:
                return record
        return None
    # some random comment
    @staticmethod
    async def create_usage_record(record: UsageRecord, user: Users):
        sheet =  UsageRecordsController.sheet
        next_id = await utilities.get_next_id(sheet)
        user_id = user["id"]
        UsageRecordsController.sheet.append_row([
            next_id, user_id, record.period_start, record.period_end, record.migration_used,
            record.realtime_used, record.created_at, record.updated_at
        ])
        return {"message": "Usage record created successfully"}

    @staticmethod
    async def update_usage_record(record_id: int, record: UsageRecord, user: Users):
        sheet =  UsageRecordsController.sheet
        next_id = await utilities.get_next_id(sheet)
        user_id = user["id"]
        records = UsageRecordsController.sheet.get_all_records()
        for idx, rec in enumerate(records, start=2):
            if int(rec["id"]) == record_id:
                UsageRecordsController.sheet.update(f"A{idx}:H{idx}", [[
                    record_id, user_id, record.period_start, record.period_end, record.migration_used,
                    record.realtime_used, record.created_at, record.updated_at
                ]])
                return {"message": "Usage record updated successfully"}
        return {"error": "Usage record not found"}

    @staticmethod
    async def delete_usage_record(record_id: int):
        records = UsageRecordsController.sheet.get_all_records()
        for idx, rec in enumerate(records, start=2):
            if int(rec["id"]) == record_id:
                UsageRecordsController.sheet.delete_row(idx)
                return {"message": "Usage record deleted successfully"}
        return {"error": "Usage record not found"}
