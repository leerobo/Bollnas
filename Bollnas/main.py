"""Main file for the FastAPI Template."""

import sys,os
from collections.abc import AsyncGenerator,AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from rich import print as rprint
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path 

from Bollnas.config.helpers import get_api_version, get_project_root
from Bollnas.config.settings import get_settings,get_controller_settings,get_sensorhub_settings
from Bollnas.database.db import async_session
import Bollnas.models.enums as enums
from Bollnas.managers import pollSensors
from Bollnas.schemas.response.gpio  import GPIOresponse

from Bollnas.blueprint import controller, sensorhub, home

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


# Load router URL paths depending on the settings
if os.environ['LOADTYPE'].lower() == 'controller':
   rprint("[blue]INFO:     [/blue][bold]Loaded Controller Routing",get_controller_settings().controller_name)
   app.include_router(controller.router)

elif os.environ['LOADTYPE'].lower() == 'sensorhub':
   rprint("[blue]INFO:     [/blue][bold]Loaded SensorHub", get_sensorhub_settings().sensorhub_name)
   app.include_router(sensorhub.router)

else:
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
