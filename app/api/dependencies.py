from fastapi import Depends
from app.core.config import get_settings

def get_api_key(settings: dict = Depends(get_settings)):
    return settings.API_KEY

def get_user_agent(settings: dict = Depends(get_settings)):
    return settings.USER_AGENT

def get_db():
    # Placeholder for database dependency
    pass