"""Define routes for Authentication."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
from Bollnas.schemas.response.sensors import Sensors, Ping
 

from rich import print as rprint
from Bollnas.config.settings import get_settings
from Bollnas.managers import pollSensors
import Bollnas.models.enums as enums

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["Controller"])

@router.get("/info",status_code=status.HTTP_200_OK,
    name="Ping SensonHub",
    response_model=Ping
)
def ping():
    rtn= Ping(name=get_settings().api_title, 
                description=get_settings().api_description, 
                devicetype=enums.DeviceType.sensorhub
               )
    print(rtn)
    return rtn

@router.get("/poll",status_code=status.HTTP_200_OK,
    name="Poll Sensor Status",
    response_model=Sensors
)
async def poll():
    """ Force Poll of all attached sensors and store values , return findings """
    await pollSensors.poll()
    return Sensors()
