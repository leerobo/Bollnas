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

from Bollnas.config.helpers import get_api_version, get_project_root
from Bollnas.config.settings import get_settings
from Bollnas.database.db import async_session

from fastapi import APIRouter
from Bollnas.blueprint import controller, sensorhub, home, config_error

app = FastAPI(
    title=get_settings().api_title,
    description=get_settings().api_description,
    redoc_url=None,
    docs_url=f"{get_settings().api_root}/docs",
    #license_info=get_settings().license_info,
    contact=get_settings().contact,
    version=get_api_version(),
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)

# Load router URL paths depending on the settings
#api_router = APIRouter(prefix=get_settings().api_root)
if get_settings().load_controller:
   rprint("[blue]INFO:     [/blue][bold]Loaded Controller Routing")
   app.include_router(controller.router)

if get_settings().load_sensorhub:
   rprint("[blue]INFO:     [/blue][bold]Loaded SensorHub")
   app.include_router(sensorhub.router)

if not get_settings().load_sensorhub and not get_settings().load_controller:
   print('Load : No Router Loaded ')
   rprint("[red]ERROR:   [/red][bold]No Routing Loadded")
   app.include_router(home.router)

static_dir = get_project_root() / "static"

# set up CORS
cors_list = (get_settings().cors_origins).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
