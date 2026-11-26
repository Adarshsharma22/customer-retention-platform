"""
Unit Tests for Database Configuration and Safe Credential Handling.
"""

import os
import pytest
from python.config.db_config import get_connection_parameters, get_db_url


def test_connection_parameters_never_expose_password():
    """Ensures get_connection_parameters masks the actual password."""
    params = get_connection_parameters()
    assert "password" not in params
    assert "password_configured" in params
    assert isinstance(params["password_configured"], bool)
    assert params["database"] == "customer_retention_db"
    assert params["user"] == "postgres"


def test_db_url_format():
    """Validates PostgreSQL SQLAlchemy connection string formatting."""
    url = get_db_url()
    assert url.startswith("postgresql+psycopg2://")
    assert "customer_retention_db" in url
    assert "localhost" in url
