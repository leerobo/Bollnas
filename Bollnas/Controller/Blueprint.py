"""Define routes for Authentication."""
# import os
from typing import Annotated, Union

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from rich import print as rprint                          ## Pretty Print
import requests, datetime

from Common.Managers.hubScanner import scan_lan       ## Hub Scanners
import Common.Managers.redis as redis                 
from Common.Config import getConfig

#from Common.Schemas.cached import Controller              ## Schemas
import Common.Schemas.scannerHubs as Hubs
import Common.Schemas.poll as Poll
import Common.Schemas.poll as FullPoll
import Common.Models.enums as enums
#import Common.Schemas.sensors as Sensors

import prometheus_client as prom 
from prometheus_client import Enum, Counter, Gauge, Histogram 

router = APIRouter(tags=["Controller"])

@router.get("/scan",status_code=status.HTTP_200_OK,
    name="Scan Lan for SensorHubs",
    response_model=Hubs.Hubs
)
async def scan():
    """
    Scan Lan finding attached Sensor Hubs based on the sensorHub port number
    - **netgear**: If a Netgear Router , then set password to gain access to the router to extract attached devices.
    - **LanScan**: Scan sequencally thru the IP range of DNS 

    LanScan can take up to 2 mins to complete,  Netgear scann can take up to a minute to complete
    """
    cacheKey='HubCache'
    Hubs=scan_lan()
    await redis.set_cache(data=Hubs,keys=cacheKey,dur=getConfig().redisHubTimer)
    rprint('[yellow]SCAN     [/yellow] SensorHub Scanner Refreshed')
    return Hubs
    # TODO: store hubs to a generic thread safe area 


@router.get("/hubs",status_code=status.HTTP_200_OK,    
    response_model=Poll.FullPoll,
    name="response with sensorhub sensors and update Metrics"
)
async def scan_hubs():                                      #  Scan Available sensorHubs and return responses 
    """
    Responses all attached SensorHubs information and setups the metrics formatted collections
    """    
    cacheKey='HubCache'
    try:
       if await redis.exists(cacheKey) == 0:                #  Scan for Hubs if Cache has expired
          scannHub = scan_lan()
          await redis.set_cache(data=scannHub,keys=cacheKey,dur=getConfig().redisHubTimer) 
       else:   
          scannHub=Hubs.Hubs(**await redis.get_cache(cacheKey))

    except Exception as ex:
       rprint("[yellow]CNTL:     [/yellow][red]Redis not Available - Dynamic Scanner")
       scannHub = scan_lan()
    
    rtn=Poll.FullPoll(timestamp=str(datetime.datetime.now()) ,polls={})
    for getHubs in scannHub.SensorHubs:
      try:
          if await redis.exists(getHubs.name) == 0:                #  Scan for Hubs sensor details if Cache has expired
            sensorsRtn=requests.get(url='http://{}:{}/poll'.format(getHubs.ip,getConfig().sensorHub_port))
            sensorSchema=Poll.Poll(**sensorsRtn.json())
            await redis.set_cache(data=sensorSchema,keys=getHubs.name)
          else:  
            cachedData=await redis.get_cache(keys=getHubs.name)
            sensorSchema=Poll.Poll(**cachedData)
            
      except Exception as ex:
            rprint("[yellow]CNTL:     [/yellow][red]Dynamic Polling[/red]",ex)
            sensorsRtn=requests.get(url='http://{}:{}/poll'.format(getHubs.ip,getConfig().sensorHub_port))
            sensorSchema=Poll.Poll(**sensorsRtn.json())

      # set up metrics
      # rprint("[purple]CNTL:     [/purple]",getHubs.ip,'--',type(sensorSchema),sensorSchema)

      rtn.polls[getHubs.name]=sensorSchema
      #rtn[getHubs.name]=sensorSchema

      # ---- Setup metrics    TODO : Needs some work
      for pins in sensorSchema.GPIOsettings:
         if pins.status == enums.GPIOstatus.ok:
            if pins.description != '': SubDesc='P'+str(pins.pin)+'-'+pins.description
            else : SubDesc='P'+str(pins.pin)
            try:
               regName=getHubs.name+'_GPIO_'+SubDesc
               if regName in prom.REGISTRY._names_to_collectors:
                  e =  prom.REGISTRY._names_to_collectors[regName]
               else: 
                  e = Enum(name=SubDesc,
                     namespace=getHubs.name,
                     subsystem='GPIO',
                     documentation='Pin_{}'+format(pins.pin),
                     states=['on', 'off']
                    )
                  if pins.value == 0 :  e.state('on')            
                  else :                e.state('off')
            except Exception as ex:
               rprint("[red]CNTL:     [/red]",regName,':',ex)

      for W1 in sensorSchema.wire1Sensors:
            if W1.description != '': SubDesc=W1.id+'_'+W1.description
            else : SubDesc=W1.id
            try:
               regName=getHubs.name+'_WIRE1_'+SubDesc
               if regName in prom.REGISTRY._names_to_collectors:
                  es =  prom.REGISTRY._names_to_collectors[regName]
               else: 
                  es = Gauge(name=SubDesc,
                     namespace=getHubs.name,
                     subsystem='WIRE1',
                     documentation=str(W1.type.name)+'-'+str(W1.measurement.value)
                    )
               es.set(W1.value)            
            except Exception as ex:
               rprint("[red]CNTL:     [/red]",regName,':',ex)
      
    # rprint("[purple]CNTL:     [/purple]Return >>>>> ",rtn)
    return rtn


   