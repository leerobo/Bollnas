from fastapi import FastAPI
from pydantic import BaseModel
from DataStructures import dsSensorHub

app = FastAPI()

"""
  Designed to sit on a RPI under a generic local Port Number (14211) and return 
  Sensor information and carry out Relay requests 
"""

@app.get("/info")         # Port Ping
def ping_Info():
    rtn=dsSensorHub.respPing(name="Hub 1",description="Boiler")
    # place Device Info get Here
    rtn.attached=0
    rtn.devices=[{"Message":"None Attached"}]   
    return rtn

@app.get("/sensors")         # Port Ping
def getSensors():
    rtn=dsSensorHub.respSensors()
    return rtn

@app.get("/sensor/{item_id}")         # Port Ping
def getSensor(item_id: str | None = None):
    rtn=dsSensorHub.respSensor(id=item_id,description="Boiler Temp",type=1,value=0)
    return rtn

