import redis
from pydantic_settings import BaseSettings, SettingsConfigDict
# from Common.Models.cached import  Controller,Sensorhub,Sensor
from Common.Config import getConfig
import datetime,json
from rich import print as rprint

r = redis.Redis(host='localhost', port=6379, db=0)

async def set_cache(data: object, keys='bollnas',dur=0):
    try:
        if dur == 0 : dur = getConfig().redisTimer
        rprint("[orange3]CNTL:     [/orange3][yellow]Cached",keys,'[yellow]for',dur,'[yellow]Seconds')
        r.set(keys, data.model_dump_json(),ex=dur)
    except Exception as e:
        rprint("[red]CNTL:     [/red][yellow]Cached Error",e)
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

async def exists(key):
     return r.exists(key)
