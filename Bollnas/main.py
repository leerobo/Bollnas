"""Main file for the FastAPI Template."""

import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from rich import print as rprint
from sqlalchemy.exc import SQLAlchemyError

from config.helpers import get_api_version, get_project_root
from config.settings import get_settings
from database.db import async_session

from fastapi import APIRouter
from blueprint import config_error
from blueprint import controller, sensorhub, home

app = FastAPI(
    title=get_settings().api_title,
    description=get_settings().api_description,
    redoc_url=None,
    docs_url=f"{get_settings().api_root}/docs",
    license_info=get_settings().license_info,
    contact=get_settings().contact,
    version=get_api_version(),
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)


api_router = APIRouter(prefix=get_settings().api_root)
api_router.include_router(controller.router)
api_router.include_router(sensorhub.router)

# set up CORS
cors_list = (get_settings().cors_origins).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
