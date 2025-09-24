from pydantic import BaseModel
from typing import Optional

class UsageRecord(BaseModel):
    period_start: str
    period_end: str
    migration_used: int
    realtime_used: int
    created_at: str
    updated_at: str
