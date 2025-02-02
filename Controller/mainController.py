"""Main file for the FastAPI Template."""

import sys, os
from collections.abc import AsyncGenerator,AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rich import print as rprint

from .ConfigController.settings  import get_settings
from .Blueprint import controller 
from redis import asyncio as aioredis

sys.path.append(os.path.abspath("./"))
from Common.Config.helpers import get_api_version, get_project_root

#from Common.Managers import pollSensors
from Common.Schemas.response.gpio  import  GPIOresponse
import Common.Models.enums as enums

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
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
rprint("[green]INFO:     [blue][bold]Loaded Controller ")
app.include_router(controller.router)

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
