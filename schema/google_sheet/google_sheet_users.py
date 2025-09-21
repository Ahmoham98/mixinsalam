from pydantic import BaseModel

class Users (BaseModel):
    mixin_access_token: str
    basalam_access_token: str
    email: str
    created_at: str
    updated_at: str
    is_active: str
    role: str
    is_verified: bool