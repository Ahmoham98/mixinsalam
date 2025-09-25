from pydantic import BaseModel
from typing import Optional

class Payment(BaseModel):
    subscription_id: int
    amount: float
    currency: str
    status: str
    payment_provider: str
    provider_payment_id: str
    invoice_url: Optional[str]
    created_at: str
    updated_at: str
