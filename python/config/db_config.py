"""
Database configuration and connection management module.
Reads configuration from environment variables / .env safely.
"""

import os
from urllib.parse import quote_plus
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
import psycopg2

# Automatically locate and load .env file from workspace root or current directory
_env_path = find_dotenv(usecwd=True)
if _env_path:
    load_dotenv(_env_path)
else:
    load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "customer_retention_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_connection_parameters():
    """Returns database parameters dictionary without exposing the raw password."""
    return {
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME,
        "user": DB_USER,
        "password_configured": bool(DB_PASSWORD),
    }


def get_db_url():
    """Constructs SQLAlchemy database URL with properly escaped credentials."""
    safe_user = quote_plus(DB_USER)
    safe_pass = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    return f"postgresql+psycopg2://{safe_user}:{safe_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_sqlalchemy_engine(echo=False, pool_size=5, max_overflow=10):
    """Creates a SQLAlchemy engine using pooled connections."""
    url = get_db_url()
    return create_engine(url, echo=echo, pool_size=pool_size, max_overflow=max_overflow)


def get_raw_connection():
    """Creates a direct psycopg2 connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5,
    )
