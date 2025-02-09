"""Main file for the FastAPI Template."""

import sys, os
from collections.abc import AsyncGenerator,AsyncIterator
from contextlib import asynccontextmanager
#from typing import Any,Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

from rich import print as rprint

import SensorHub.Blueprint as bluePrint
import SensorHub.Managers.pollSensors as pollSensors

from  SensorHub.Config import getConfig
import Common.Schemas.Sensors.wire1 as wire1
import Common.Schemas.Sensors.gpio as gpio
import Common.Models.enums as enums
from Common.Config.helpers import get_api_version, get_project_root, get_api_details


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    rprint('Reset Relays :',getConfig().GPIOrelays)
    for relay in getConfig().GPIOrelays:
        pollSensors.GPIOset( gpio.Pins(pin=relay,pintype=enums.GPIOdeviceAttached.relay,direction=enums.GPIOdirection.out), task=enums.GPIOtask.off )
    yield

app = FastAPI(
    title=getConfig().api_title,
    description=getConfig().api_description,
    redoc_url=None,
    docs_url=f"{getConfig().api_root}/docs",
    #license_info=get_settings().license_info,
    contact=getConfig().contact,
    version=get_api_version(),
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
    lifespan=lifespan
)

rprint("[orange3]CNTL:     [/orange3]Loaded SensorHub ")
app.include_router(bluePrint.router)

static_dir = get_project_root() / "static"

# set up CORS
cors_list = (getConfig().cors_origins).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
