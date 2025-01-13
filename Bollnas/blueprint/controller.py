"""Define routes for Authentication."""

from typing import Annotated, Union

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
# from Bollnas.managers.auth import AuthManager
# from Bollnas.managers.user import UserManager
from Bollnas.schemas.response import sensor_hubs

from Bollnas.managers.scanner import scan_lan

 
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from Bollnas.models.cached import Controller
import Bollnas.cachecontrol.redis as redis

router = APIRouter(tags=["Controller"])

@router.get("/scan",status_code=status.HTTP_200_OK,
    name="Scan Lan for SensorHubs",
    response_model=sensor_hubs.SensorHubs
)
async def scan():
    devices = scan_lan()
    for device in devices:
       print(f"IP: {device['ip']}, MAC: {device['mac']}")
    return sensor_hubs.SensorHubs(count=len(devices),Hubs=list(devices))
    # TODO: store hubs to a generic thread safe area 
    

@router.get("/hubs",status_code=status.HTTP_200_OK,
    name="show attached active hubs",
    response_model=Controller
)
async def scan_hubs() -> Controller:
    try:
       c = await redis.get_cache('bollnas') 
    except:
       c = redis.test_hub()   
       await redis.set_cache(redis.test_hub())
       c = await redis.get_cache('bollnas') 
       print('Test Cache Set')
    return Controller.model_validate(c)







