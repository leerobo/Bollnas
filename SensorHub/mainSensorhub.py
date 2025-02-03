"""Main file for the FastAPI Template."""

import sys, os
from collections.abc import AsyncGenerator,AsyncIterator
from contextlib import asynccontextmanager
#from typing import Any,Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

from rich import print as rprint
# from sqlalchemy.exc import SQLAlchemyError
# from pathlib import Path 

import Common.Models.enums as enums
from Common.Config.helpers import get_api_version, get_project_root
from Common.Managers import pollSensors
from Common.Schemas.response.gpio  import GPIOresponse

from .ConfigSensorhub.settings import get_settings
from .Blueprint import sensorhub

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
    
from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    rprint('Reset Relays :',get_settings().GPIOrelays)
    for relay in get_settings().GPIOrelays:
        pollSensors.GPIOset( GPIOresponse(pin=relay,pintype=enums.GPIOdeviceAttached.relay,direction=enums.GPIOdirection.out), task=enums.GPIOtask.off )
    yield

app = FastAPI(
    title=get_settings().api_title,
    description=get_settings().api_description,
    redoc_url=None,
    docs_url=f"{get_settings().api_root}/docs",
    #license_info=get_settings().license_info,
    contact=get_settings().contact,
    version=get_api_version(),
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
    lifespan=lifespan
)

rprint("[blue]INFO:     [/blue][bold]Loaded SensorHub")
app.include_router(sensorhub.router)

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
