import os
from dotenv import load_dotenv

load_dotenv()

def normalize_database_url(url: str | None) -> str | None:
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///blacklist.db")
    #SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv("DATABASE_URL"))
    STATIC_BEARER_TOKEN = os.getenv("STATIC_BEARER_TOKEN", "super-token-123")
    TESTING = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv("DEV_DATABASE_URL", "sqlite:///blacklist_dev.db")
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    STATIC_BEARER_TOKEN = os.getenv("TEST_STATIC_BEARER_TOKEN", "test-token-123")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv("DATABASE_URL")
    )