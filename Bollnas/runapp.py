"""Main file for the FastAPI Template."""

import sys, os
from collections.abc import AsyncGenerator,AsyncIterator
from contextlib import asynccontextmanager
#from typing import Any,Union

from fastapi import FastAPI,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

from rich import print as rprint
from typing import Union

from prometheus_client import make_asgi_app               ## Prometheus
from prometheus_client import multiprocess
import prometheus_client as prom

import SensorHub.Blueprint as SensorhubRouter
import Controller.Blueprint as ControllerRouter

import Common.Managers.pollSensors as pollSensors

from   Common.Config import getConfig, getControllerConfig, getSensorHubConfig
import Common.Schemas.Sensors.wire1 as wire1
import Common.Schemas.Sensors.gpio as gpio
import Common.Models.enums as enums
from   Common.helpers import get_api_version, get_project_root, get_api_details

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    rprint('[blue]INFO:    [/blue] Initiated Routines Running')
    for relay in getSensorHubConfig().GPIOrelays:
        pollSensors.GPIOinit( gpio.PinChange( pin=relay, task=enums.GPIOtask.off ) )
    rprint('[blue]INFO:    [/blue] Initiated Routines Complete')        
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

rprint('[blue]INFO:    [/blue] Router Settings Loading : '+str(getSensorHubConfig().GPIOrelays))
if os.getenv("CONTROLLER") == 'True' :  app.include_router(ControllerRouter.router)
if os.getenv("SENSORHUB")  == 'True' :  app.include_router(SensorhubRouter.router)

# Generic Route across both SensorHub and Controller , not advisable for Production run

@app.get("/settings/(code)",status_code=status.HTTP_200_OK, name="Show Installation Settings" ,tags=["Generic"])
async def AdminSettings(code:str ):                                   
    if code != 'Winter2BerryMoon.'  :  raise HTTPException(status_code=401, detail="Invalid Code")
    rtn = [getConfig()]
    if os.getenv("SENSORHUB")  == 'True' :  rtn.append(getSensorHubConfig())
    if os.getenv("CONTROLLER") == 'True' :  rtn.append(getControllerConfig())
    return  rtn

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Force metrics not to extract platform info
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)    # Suppress Memory/CPU usage
# prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)   # Suppress Python Version
prom.REGISTRY.unregister(prom.GC_COLLECTOR)         # Supress Collection Reg details

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
