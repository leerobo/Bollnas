"""Define routes for Authentication."""
import os
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
from prometheus_client import make_asgi_app
from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Counter, Gauge,Histogram

from Bollnas.managers import sensorClient as SC

router = APIRouter(tags=["Controller"])

# Using multiprocess collector for registry
# def make_metrics_app():
#     print('pDir',os.environ['PROMETHEUS_MULTIPROC_DIR'] )
#     registry = CollectorRegistry()
#     multiprocess.MultiProcessCollector(registry)
#     return make_asgi_app(registry=registry)


@router.get("/metrics",status_code=status.HTTP_200_OK,
    name="Prometheus Metrics Portal",
)
#def add_sample(self, name: str, labels: Dict[str, str], value: float, timestamp: Optional[Union[Timestamp, float]] = None, exemplar: Optional[Exemplar] = None) -> None:

async def metrics():
   sensors = await SC.get_sensors()
   print(sensors)
   return sensors

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







