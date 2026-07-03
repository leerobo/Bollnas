import redis
from pydantic_settings import BaseSettings, SettingsConfigDict
# from Common.Models.cached import  Controller,Sensorhub,Sensor
#from Bollnas.Common.zzzzzConfig import getConfig
from Common.ConfigLoad import getJSONconfig
import datetime,json,time
from rich import print as rprint

r = None

async def set_cache(data: object, keys='bollnas',dur=0):
    if r == None : await connect_cache()
    try:
        if dur == 0 : dur = getJSONconfig().Cache.Timer
        rprint("[orange3]CNTL:     [/orange3][yellow]Cached",keys,'[yellow]for',dur,'[yellow]Seconds')
        r.set(keys, data.model_dump_json(),ex=dur)
    except Exception as e:
        rprint("[red]CNTL:     [/red][yellow]Cached Error",e)
        print(__name__,':set:',e)
    return

async def get_cache(keys='bollnas') -> dict:
    if r == None : await connect_cache()
    try:
       v = r.get(keys)
       if v is not None:
          return json.loads(v.decode('utf-8'))
       else:
          raise Exception('Cache Key not found')
    except Exception as e:  
       raise Exception(e)

async def exists(key):
    if r == None : await connect_cache()
    return r.exists(key)

async def del_cache(key='SomeKey'):
    if r == None : await connect_cache()
    rprint("[orange3]CNTL:     [/orange3][yellow]Deleted Cache Key",key)
    r.delete(key)
    return 

async def connect_cache():
    attempts=10
    while attempts > 0:
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            rprint("[green]CNTL:     [/green][yellow]Redis Connection Established")
            return r
        except Exception as e:
            rprint("[red]CNTL:     [/red][yellow]Redis Connection Error",e)
            print(__name__,':init:',e)
            time.sleep(5)
            attempts -= 1
    return None

# r = await connect_cache()
# r = redis.Redis(host='localhost', port=6379, db=0)


