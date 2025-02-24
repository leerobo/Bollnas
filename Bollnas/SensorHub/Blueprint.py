"""Define routes for Authentication."""
from typing import Annotated,Union

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# from Common.database.db import get_database
import Common.Schemas.ping as Ping
import Common.Schemas.Sensors.wire1 as wire1
import Common.Schemas.Sensors.gpio as gpio
import Common.Schemas.error as error

from rich import print as rprint
from  Common.Config import getConfig
import Common.Managers.pollSensors as pollSensors
import Common.Models.enums as enums

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["sensorHub"])

@router.get("/ping",status_code=status.HTTP_200_OK,
    name="Ping SensonHub Gateway",
    description='Ping Device and return back descriptive information',    
    response_model=Ping.PingResponse
)
def ping():
    return Ping.PingResponse(name=getConfig().api_title, 
              description=getConfig().api_description, 
              location=getConfig().api_location, 
              devicetype=enums.DeviceType.sensorhub,
              security=getConfig().security,
              securityKey=getConfig().securityKey,
              wire1=getConfig().wire1,
              relays=getConfig().relays,
              zigbee=getConfig().zigbee
            )


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
        response_model=Union[gpio.Pins,list[gpio.Pins],error.response]
)
def relay(task:gpio.PinChange):
    if len(getConfig().GPIOrelays) == 0 :
       return error.response(message='No Relay Pin Defined for this Device')
        
    if task.pin == 0:  
       rtn=[]
       for relay in getConfig().GPIOrelays:
           rtn.append(pollSensors.GPIOset( task ) )
       return rtn

    if task.pin not in getConfig().GPIOrelays:
       return error.response(message='Pin not Defined as Relay - see GPIOrelays in settings')

    return pollSensors.GPIOset( pollSensors.GPIOset( task ))

@router.get("/poll",status_code=status.HTTP_200_OK,
    name="Poll Sensor Status",
    description='Force a Poll on all Attached Sensors & Switches and cache results',
    response_model=dict
)
async def poll():
    """ Force Poll of all attached sensors and store values , return findings """
    return await pollSensors.poll()

