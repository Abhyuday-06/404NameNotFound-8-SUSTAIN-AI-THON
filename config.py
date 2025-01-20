import os
from dotenv import load_dotenv
import secrets

load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))  # Use .env value or generate a fallback key
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///data.db",  # Fallback to SQLite for local development if DATABASE_URL isn't set
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    ENV = 'production'
