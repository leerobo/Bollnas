"""Define routes for Authentication."""

from typing import Annotated,Union

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
from Bollnas.schemas.response.sensors import Sensors, Ping
from Bollnas.schemas.response.gpio  import GPIOresponse
from Bollnas.schemas.response.error import ErrorResponse
from Bollnas.schemas.request.gpio import GPIOrequest
 

from rich import print as rprint
from Bollnas.config.settings import get_settings
from Bollnas.managers import pollSensors
import Bollnas.models.enums as enums

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["Controller"])

@router.get("/info",status_code=status.HTTP_200_OK,
    name="Ping SensonHub",
    description='Ping Device and return back descriptive information',    
    response_model=Ping
)
def ping():
    rtn= Ping(name=get_settings().api_title, 
                description=get_settings().api_description, 
                devicetype=enums.DeviceType.sensorhub,
                relays=get_settings().GPIOrelays
               )
    print(rtn)
    return rtn

@router.get("/poll",status_code=status.HTTP_200_OK,
    name="Poll Sensor Status",
    description='Force a Poll on all Attached Sensors & Switches and cache results',
    response_model=dict
)
async def poll():
    """ Force Poll of all attached sensors and store values , return findings """
    return await pollSensors.poll()

@router.post("/relay",status_code=status.HTTP_200_OK,
    name="Relay Control ",
    description='Relay controller to toggle,switch on or off GPIO Pins',
    response_model=Union[GPIOresponse,list[GPIOresponse],ErrorResponse]
)
def relay(task:GPIOrequest):
    if task.pin == 0:  # Carry out task on all Relays
       rtn=[]
       for relay in get_settings().GPIOrelays:
          rtn.append(pollSensors.GPIOset( GPIOresponse(pin=relay,pintype=enums.GPIOdeviceAttached.relay,direction=enums.GPIOdirection.out), task=task.task ))
       return rtn
    
    if task.pin not in get_settings().GPIOrelays:
       return ErrorResponse(message='Pin not Defined as Relay - see GPIOrelays in settings')
    return pollSensors.GPIOset( GPIOresponse(pin=task.pin,pintype=enums.GPIOdeviceAttached.relay,direction=enums.GPIOdirection.out), task=task.task )
