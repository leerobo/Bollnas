"""Define routes for Authentication."""
from typing import Annotated,Union
import os, pathlib   


from fastapi import APIRouter, BackgroundTasks, Depends, status, Header
 
from sqlalchemy.ext.asyncio import AsyncSession

# from Common.database.db import get_database
import Common.Schemas.ping as Ping
import Common.Schemas.Sensors.wire1 as wire1
import Common.Schemas.Sensors.gpio as gpio
import Common.Schemas.error as error
import Common.Schemas.HTTPheaders as HTTPheaders

from rich import print as rprint
#from  Bollnas.Common.zzzzzConfig import getConfig,getSensorHubConfig
from Common.ConfigLoad import getJSONconfig
import Common.Managers.pollSensors as pollSensors
import Common.Models.enums as enums
import Common.Schemas.poll as Pollschema

from dotenv import load_dotenv
from Common.Managers import decorators

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["SensorHub"])

@router.get("/ping",status_code=status.HTTP_200_OK,
    name="Ping SensonHub Gateway",
    description='Ping Device and return back descriptive information',    
    response_model=Ping.PingResponse
)
def ping():
    rprint(getJSONconfig())
    rtn = Ping.PingResponse(name=getJSONconfig().Title, 
              description=getJSONconfig().Description, 
              location=getJSONconfig().Installation.Location, 
              devicetype=enums.DeviceType.sensorhub,
              security=getJSONconfig().Security.comms,
              wire1=getJSONconfig().SensorHubs.Wire1,
              zigbee=getJSONconfig().SensorHubs.Zigbee
            )
    if getJSONconfig().Security.Comms == True :
        if ( getJSONconfig().Security.apikey != "" ) :
            rtn.securityKey = getJSONconfig().Security.apikey
        elif ( getJSONconfig().Security.pemCert != "" ) :
            rtn.securityKey = getJSONconfig().Security.pemCert

    if getJSONconfig().SensorHubs.Relays != [] :       
        rtn.relays=True

    return rtn
             
@router.get("/poll",status_code=status.HTTP_200_OK,
    name="Poll Sensor Status",
    description='Force a Poll on all Attached Sensors & Switches and cache results',
    response_model=Pollschema.Poll
)
@decorators.token_required
async def poll( headers: Annotated[HTTPheaders.Headers, Header()] ):
    """ Force Poll of all attached sensors and store values , return findings """
    return await pollSensors.poll()

@router.post("/relay",status_code=status.HTTP_200_OK,
     name="Relay Control ",
        description='Relay controller to toggle,switch on or off GPIO Pins',
        response_model=Union[gpio.Pins,list[gpio.Pins],error.response]
)
@decorators.token_required
def relay(task:gpio.PinChange):
    if len(getSensorHubConfig().GPIOrelays) == 0 :
       return error.response(message='No Relay Pin Defined for this Device')
        
    if task.pin == 0:  
       rtn=[]
       for relay in getSensorHubConfig().GPIOrelays:
           task.pin = relay
           rtn.append(pollSensors.GPIOset( task ) )
       return rtn

    if task.pin not in getSensorHubConfig().GPIOrelays:
       return error.response(message='Pin not Defined as Relay - see GPIOrelays in settings')

    return  pollSensors.GPIOset( task )

@router.get("/settings",status_code=status.HTTP_200_OK,
    name="Sensorhub Settings",
    description='Show sensorhub control settings',
    response_model=dict
)
@decorators.token_required
async def get_settings(headers: Annotated[HTTPheaders.Headers, Header() ]):
    """ get sensorhub settings """
    return getJSONconfig().model_dump(exclude_defaults=True,exclude_none=True)
