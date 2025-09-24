from schema.google_sheet.payments import Payment
from google_sheet_configuration import spreadsheet

class PaymentsController:
    sheet = spreadsheet.worksheet("payments")

    @staticmethod
    async def get_all_payments():
        records = PaymentsController.sheet.get_all_records()
        return records

    @staticmethod
    async def get_payment_by_id(payment_id: int):
        records = PaymentsController.sheet.get_all_records()
        for record in records:
            if int(record["id"]) == payment_id:
                return record
        return None

    @staticmethod
    async def create_payment(payment: Payment):
        PaymentsController.sheet.append_row([
            payment.id, payment.user_id, payment.subscription_id, payment.amount, payment.currency, payment.status,
            payment.payment_provider, payment.provider_payment_id, payment.invoice_url, payment.created_at, payment.updated_at
        ])
        return {"message": "Payment created successfully"}

    @staticmethod
    async def update_payment(payment_id: int, payment: Payment):
        records = PaymentsController.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == payment_id:
                PaymentsController.sheet.update(f"A{idx}:K{idx}", [[
                    payment.id, payment.user_id, payment.subscription_id, payment.amount, payment.currency, payment.status,
                    payment.payment_provider, payment.provider_payment_id, payment.invoice_url, payment.created_at, payment.updated_at
                ]])
                return {"message": "Payment updated successfully"}
        return {"error": "Payment not found"}

    @staticmethod
    async def delete_payment(payment_id: int):
        records = PaymentsController.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == payment_id:
                PaymentsController.sheet.delete_row(idx)
                return {"message": "Payment deleted successfully"}
        return {"error": "Payment not found"}
