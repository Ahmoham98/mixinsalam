from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)

class Settings(BaseSettings):
    # Environment Switch: Reads APP_ENV from the environment variables.
    # Defaults to "development" if not set.
    APP_ENV: str = "development"

    # Shared settings
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
   
    # --- Basalam Production Credentials ---
    BASALAM_PROD_CLIENT_ID: str
    BASALAM_PROD_CLIENT_SECRET: str
    BASALAM_PROD_REDIRECT_URI: str

    # --- Basalam Development Credentials ---
    BASALAM_DEV_CLIENT_ID: str
    BASALAM_DEV_CLIENT_SECRET: str
    BASALAM_DEV_REDIRECT_URI: str
    
    # --- DYNAMIC CREDENTIALS (The rest of the app will only use these) ---
    BASALAM_CLIENT_ID: str = ""
    BASALAM_SECRET: str = ""
    BASALAM_REDIRECT_URI: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# --- Instantiate the settings ---
Config = Settings()

# --- Dynamically set the correct credentials based on APP_ENV ---
if Config.APP_ENV == "production":
    print("✅ Loading PRODUCTION settings...")
    Config.BASALAM_CLIENT_ID = Config.BASALAM_PROD_CLIENT_ID
    Config.BASALAM_SECRET = Config.BASALAM_PROD_CLIENT_SECRET
    Config.BASALAM_REDIRECT_URI = Config.BASALAM_PROD_REDIRECT_URI
    # print(f"client id: {Config.BASALAM_CLIENT_ID}")
    # print(f"client secret: {Config.BASALAM_SECRET}")
    # print(f"redirect uri: {Config.BASALAM_REDIRECT_URI}")
else: # Default to development
    print("🛠️  Loading DEVELOPMENT settings...")
    Config.BASALAM_CLIENT_ID = Config.BASALAM_DEV_CLIENT_ID
    Config.BASALAM_SECRET = Config.BASALAM_DEV_CLIENT_SECRET
    Config.BASALAM_REDIRECT_URI = Config.BASALAM_DEV_REDIRECT_URI
    # print(f"client id: {Config.BASALAM_CLIENT_ID}")
    # print(f"client secret: {Config.BASALAM_SECRET}")
    # print(f"redirect uri: {Config.BASALAM_REDIRECT_URI}")