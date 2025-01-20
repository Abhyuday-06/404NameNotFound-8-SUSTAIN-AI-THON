import os
import secrets

secret = secrets.token_hex(32)
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", secret)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
