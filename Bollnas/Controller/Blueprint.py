"""Define routes for Authentication."""
# import os
from typing import Annotated, Union

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from rich import print as rprint                          ## Pretty Print
import requests, datetime, traceback

from Common.Managers.hubScanner import scan_lan       ## Hub Scanners
import Common.Managers.redis as redis                 
#from Bollnas.Common.zzzzzConfig import getConfig,getControllerConfig
from Common.ConfigLoad import getJSONconfig

#from Common.Schemas.cached import Controller              ## Schemas
import Common.Schemas.scannerHubs as Hubs
import Common.Schemas.poll as Poll
import Common.Schemas.poll as FullPoll
import Common.Models.enums as enums
import Common.Managers.Metrics as promethuesMetrics
#import Common.Schemas.sensors as Sensors

import prometheus_client as prom 
from prometheus_client import Enum, Counter, Gauge, Histogram 
from prometheus_client.metrics import _build_full_name

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

    await redis.set_cache(data=Hubs,keys=cacheKey,dur=getJSONconfig().Cache.HubTimer)
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
    print('--Controller Hubs')
    cacheKey='HubCache'
    try:
       if await redis.exists(cacheKey) == 0:                #  Scan for Hubs if Cache has expired
          scannHub = scan_lan()
          await redis.set_cache(data=scannHub,keys=cacheKey,dur=getJSONconfig().Cache.HubTimer) 
       else:   
          scannHub=Hubs.Hubs(**await redis.get_cache(cacheKey))

    except Exception as ex:
       rprint("[yellow]CNTL:     [/yellow][red]Redis not Available - Dynamic Scanner",ex)
       scannHub = scan_lan()
    
    rtn=Poll.FullPoll(timestamp=str(datetime.datetime.now()) ,polls={})
    for getHubs in scannHub.SensorHubs:
      try:
          if await redis.exists(getHubs.name) == 0:                #  Scan for Hubs sensor details if Cache has expired
            sensorsRtn=requests.get(url='http://{}:{}/poll'.format(getHubs.ip,getJSONconfig().ControllerHub.Port_Scanner))
            sensorSchema=Poll.Poll(**sensorsRtn.json())
            print('Refresh Redis Cache Scan')
            await redis.set_cache(data=sensorSchema,keys=getHubs.name)
          else:  
            print('Redis Cache Scan')
            cachedData=await redis.get_cache(keys=getHubs.name)
            sensorSchema=Poll.Poll(**cachedData)
            
      except Exception as ex:
            rprint("[yellow]CNTL:     [/yellow][red]Dynamic Polling[/red]",ex)
            sensorsRtn=requests.get(url='http://{}:{}/poll'.format(getHubs.ip,getJSONconfig().ControllerHub.Port_Scanner))
            sensorSchema=Poll.Poll(**sensorsRtn.json())

      rtn.polls[sensorSchema.hubName+'_'+sensorSchema.subHubName]=sensorSchema

      # Set Prometheus Metrics if Required
      if getJSONconfig().metric_required:
         promethuesMetrics.setPrometheusMetrics(sensorSchema) 

    return rtn


   