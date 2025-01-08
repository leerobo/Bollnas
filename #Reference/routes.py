"""Include all the other routes into one router."""

from fastapi import APIRouter

from Bollnas.config.settings import get_settings
import controller, sensorhub, home
api_router = APIRouter(prefix=get_settings().api_root)

api_router.include_router(controller.router)
api_router.include_router(sensorhub.router)

if not get_settings().no_root_route:
    api_router.include_router(home.router)
