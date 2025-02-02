"""Define the network scanner manager."""
from __future__ import annotations

from rich import print as rprint
from Bollnas.cachecontrol.redis import get_cache
from prometheus_client import metrics,Gauge
import RPi.GPIO as gpio                 # for general GPIO control over relays

#from Bollnas.config.settings import get_settings

async def get_sensors():
    """ using the latest Polled data, setup the Sensor Client using promethues """
    try:
      sensors = await get_cache('bollnas')
    except Exception as e:
      print(e)
      return []  
    
    print(sensors)
    print('---------------------------------------------')
    print('Sensor Controller :',sensors['name'])
    print('Sensor Timestamp  :',sensors['timestamp'])
    rtn=[]

    for sh in sensors['hubs']:
        g = Gauge(sensors['name'],sh['name'])
        for s in sh['sensors']:
          print('>>> Sensors Hub:',sh['name'],s['name'])
          g.set(4.2)   # Set to a given value
          g.set_to_current_time()
          g.set_function(lambda: 5.2)  # Set to the result of a function
          rtn.append(g)
          print('G:',g.collect())        

    print(rtn)    

        
   
   #g = Gauge('my_inprogress_requests', 'Description of gauge')
   #g.set(4.2)   # Set to a given value
   #g.set_to_current_time()
   #g.set_function(lambda: 4.2)  # Set to the result of a function
   #print(g.collect())        


      
    return  None