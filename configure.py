import json
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ID: int
    REDIRECT_URI: str
    NAME: str
    BASALAM_SECRET: str
    GOOGLE_SERVICE_ACCOUNT_JSON: str
    SHEET_NAME: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    

Config = Settings()

# parse into dict when needed 
service_account_info = json.loads(Config.GOOGLE_SERVICE_ACCOUNT_JSON)