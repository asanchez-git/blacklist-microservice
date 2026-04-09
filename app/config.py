import os
from dotenv import load_dotenv

load_dotenv()

def normalize_database_url(url: str | None) -> str | None:
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    #SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///blacklist.db")
    SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_BEARER_TOKEN = os.getenv("STATIC_BEARER_TOKEN", "super-token-123")