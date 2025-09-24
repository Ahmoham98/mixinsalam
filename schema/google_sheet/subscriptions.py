from pydantic import BaseModel
from typing import Optional

class Subscription(BaseModel):
    plan_id: int
    status: str
    start_date: str
    end_date: str
    renewal_date: Optional[str]
    cancel_at_period_end: bool
    created_at: str
    updated_at: str
