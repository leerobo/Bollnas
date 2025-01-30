import redis
from pydantic_settings import BaseSettings, SettingsConfigDict
from Bollnas.models.cached import  Controller,Sensorhub,Sensor

import datetime,json

r = redis.Redis(host='localhost', port=6379, db=0)

async def set_cache(data: Controller, keys='bollnas',dur=120):
    try:
        r.set(keys, data.model_dump_json(),ex=dur)
    except Exception as e:
        print(__name__,':set:',e)
    return

async def get_cache(keys='bollnas') -> dict:
    try:
       v = r.get(keys)
       if v is not None:
          return json.loads(v.decode('utf-8'))
       else:
          raise Exception('Cache Key not found')
    except Exception as e:  
       raise Exception(e)

 # Test setup only 
def test_hub() -> Controller:
    sensor1 = Sensor(name='Tank Hi',id='1',description='Temperature',type=1,value=20)
    sensor2 = Sensor(name='Tank Med',id='2',description='Temperature',type=1,value=30)
    sensor3 = Sensor(name='Tank Low',id='1',description='Temperature',type=1,value=25)
    hub1 = Sensorhub(name='Boiler1',mac='00:00:00:00:00:01',ip='192.168.0.10',sensors=[sensor1,sensor2])
    hub2 = Sensorhub(name='Boiler2',mac='00:00:00:00:00:02',ip='192.168.0.11',sensors=[sensor3])
    return Controller(name='Bollnas',hubs=[hub1,hub2])
  