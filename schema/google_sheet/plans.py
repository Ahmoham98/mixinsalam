from pydantic import BaseModel
from typing import Optional

class Plan(BaseModel):
    name: str
    price_monthly: float
    quota_migration: int
    quota_realtime_updates: int
    is_active: bool
    created_at: str
    updated_at: str
