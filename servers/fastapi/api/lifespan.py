from contextlib import asynccontextmanager
import os
import logging

from fastapi import FastAPI

from services.database import create_db_and_tables
from utils.get_env import get_app_data_directory_env, get_database_url_env
from utils.model_availability import (
    check_llm_and_image_provider_api_or_model_availability,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Initializes the application data directory and checks LLM model availability.

    """
    os.makedirs(get_app_data_directory_env(), exist_ok=True)

    db_url = get_database_url_env() or "sqlite (default)"
    db_display = db_url.split("@")[-1] if "@" in db_url else db_url
    print(f"[DB] Connecting to database: {db_display}", flush=True)

    try:
        await create_db_and_tables()
        print(f"[DB] ✅ Database connected and tables ready!", flush=True)
    except Exception as e:
        print(f"[DB] ❌ Database connection FAILED: {e}", flush=True)
        raise

    await check_llm_and_image_provider_api_or_model_availability()
    yield
