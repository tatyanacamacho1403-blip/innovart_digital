import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().with_name(".env"))


def _admin_ids():
    raw = os.getenv("ADMIN_USER_IDS", "")
    return {int(value.strip()) for value in raw.split(",") if value.strip().isdigit()}


class Config:
    _secret = os.getenv("SECRET_KEY")
    if not _secret and os.getenv("APP_ENV", "development").lower() == "production":
        raise RuntimeError("SECRET_KEY debe configurarse en producción")
    SECRET_KEY = _secret or "dev-secret-change-before-deploy"
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DATABASE", "InnovartDigital")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    ACCESS_TOKEN_MAX_AGE = int(os.getenv("ACCESS_TOKEN_MAX_AGE", "43200"))
    ADMIN_USER_IDS = _admin_ids()
