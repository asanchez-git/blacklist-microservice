import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///blacklist.db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_BEARER_TOKEN = os.getenv("STATIC_BEARER_TOKEN", "super-token-123")