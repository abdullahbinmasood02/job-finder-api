import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Job Finder API"
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LINKEDIN_API_KEY: str = os.getenv("LINKEDIN_API_KEY", "")
    INDEED_API_KEY: str = os.getenv("INDEED_API_KEY", "")
    GLASSDOOR_API_KEY: str = os.getenv("GLASSDOOR_API_KEY", "")
    
    # Scraping settings
    HEADLESS_BROWSER: bool = os.getenv("HEADLESS_BROWSER", "True").lower() == "true"
    WAIT_TIME: int = int(os.getenv("WAIT_TIME", "10"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()