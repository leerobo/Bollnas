"""Define routes for Authentication."""
# import os
from typing import Annotated, Union

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from rich import print as rprint                          ## Pretty Print
import requests, datetime

from Controller.Managers.hubScanner import scan_lan       ## Hub Scanners
import Controller.Managers.redis as redis                 
from Controller.Config import getConfig

#from Common.Schemas.cached import Controller              ## Schemas
import Common.Schemas.scannerHubs as Hubs
import Common.Schemas.poll as Poll
import Common.Models.enums as enums
#import Common.Schemas.sensors as Sensors

import prometheus_client as prom 
from prometheus_client import Enum, Counter, Gauge, Histogram 

router = APIRouter(tags=["Controller"])

@router.get("/scan",status_code=status.HTTP_200_OK,
    name="Scan Lan for SensorHubs",
    response_model=Hubs.Hubs,
    description="Scanned LAN for attached Sensor Hubs and cache list to allow for polling via /hubs",
)
async def scan():
    cacheKey='HubCache'
    Hubs=scan_lan()
    await redis.set_cache(data=Hubs,keys=cacheKey,dur=getConfig().redisHubTimer)
    rprint('[yellow]SCAN     [/yellow] SensorHub Scanner Refreshed')
    return Hubs
    # TODO: store hubs to a generic thread safe area 


@router.get("/hubs",status_code=status.HTTP_200_OK,    
    response_model=dict,
    name="response with sensorhub sensors and update Metrics",
    description="Poll all attached SensorHubs to responsed with attached device information if not within Cache (See redis cache timer in Config) , this also build up the prometheus metrics response ",
)
async def scan_hubs():                                      #  Scan Available sensorHubs and return responses 
    cacheKey='HubCache'
    try:
       if await redis.exists(cacheKey) == 0:                #  Scan for Hubs if Cache has expired
          scannHub = scan_lan()
          await redis.set_cache(data=scannHub,keys=cacheKey,dur=getConfig().redisHubTimer) 
       else:   
          scannHub=Hubs.Hubs(**await redis.get_cache(cacheKey))

    except Exception as ex:
       rprint('[red]Redis Error ',ex)
       return None
    
    rtn={'timestamp':str(datetime.datetime.now()) }
    for getHubs in scannHub.SensorHubs:

      if await redis.exists(getHubs.name) == 0:                #  Scan for Hubs sensor details if Cache has expired
          sensorsRtn=requests.get(url='http://{}:{}/poll'.format(getHubs.ip,getConfig().sensorHub_port))
          sensorSchema=Poll.Poll(**sensorsRtn.json())
          await redis.set_cache(data=sensorSchema,keys=getHubs.name)
          #rprint('>New>',sensorSchema)
      else:  
        try:
            cachedData=await redis.get_cache(keys=getHubs.name)
            rprint('>Cached>',cachedData)
            sensorSchema=Poll.Poll(**cachedData)
        except Exception as ex:
            rprint('[red]ERROR     [/red]Caching Error ',ex)    
            return None,400

      # set up metrics
 
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
               rprint('[red]ERROR      [/red]',regName,':',ex)    

      for W1 in sensorSchema.wire1Sensors:
            if W1.description != '': SubDesc=W1.id+'_'+W1.description
            else : SubDesc=W1.id
            try:
               regName=getHubs.name+'_WIRE1_'+SubDesc
               if regName in prom.REGISTRY._names_to_collectors:
                  e =  prom.REGISTRY._names_to_collectors[regName]
               else: 
                  e = Gauge(name=SubDesc,
                     namespace=getHubs.name,
                     subsystem='WIRE1',
                     documentation=str(W1.type.name)+'-'+str(W1.measurement.value)
                    )
                  e.set(W1.value)            
            except Exception as ex:
               rprint('[red]ERROR      [/red]',regName,':',ex)    
            
      rtn[getHubs.name]=sensorSchema

    return rtn


      



# async def get_sensors():
#     """ using the latest Polled data, setup the Sensor Client using promethues """
#     try:
#       sensors = await get_cache('bollnas')
#     except Exception as e:
#       print(e)
#       return []  
    
#     print(sensors)
#     print('---------------------------------------------')
#     print('Sensor Controller :',sensors['name'])
#     print('Sensor Timestamp  :',sensors['timestamp'])
#     rtn=[]

#     for sh in sensors['hubs']:
#         g = Gauge(sensors['name'],sh['name'])
#         for s in sh['sensors']:
#           print('>>> Sensors Hub:',sh['name'],s['name'])
#           g.set(4.2)   # Set to a given value
#           g.set_to_current_time()
#           g.set_function(lambda: 5.2)  # Set to the result of a function
#           rtn.append(g)
#           print('G:',g.collect())        

#     print(rtn)    

        
   
#    #g = Gauge('my_inprogress_requests', 'Description of gauge')
#    #g.set(4.2)   # Set to a given value
#    #g.set_to_current_time()
#    #g.set_function(lambda: 4.2)  # Set to the result of a function
#    #print(g.collect())        


      
#     return  None



#     print()
#     rprint(scannHub)


#     return scannHub
 

