"""Main file for the FastAPI Template."""

import sys, os
from collections.abc import AsyncGenerator,AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app               ## Prometheus
from prometheus_client import multiprocess
import prometheus_client as prom

from rich import print as rprint

from Controller.Config import getConfig
import Controller.Blueprint as bluePrint

sys.path.append(os.path.abspath("./"))
from Common.Config.helpers import get_api_version, get_project_root

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
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

# Load router URL paths depending on the settings
rprint("[green]INFO:     [blue][bold]Loaded Controller ")
app.include_router(bluePrint.router)

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
