from fastapi import FastAPI
from pydantic import BaseModel
from DataStructures import dsSensorHub

app = FastAPI()


app = FastAPI(
    title="Sensor HUB API",
    description="Sensor HUB API designed for RPI deployment",
    summary="Sensor HUB",
    version="0.0.1",
    contact={
        "name": "Lee Robinson",
        "email": "lee@ssshhhh.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

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

@app.get("/logon",status_code=204)         # Logon
def logon():
    # return JWT Token
    return 

@app.get("/sensors",response_model=dsSensorHub.respSensor)                  # List ALL sensors
def getSensors():
    rtn=dsSensorHub.respSensors()
    return rtn

@app.get("/sensor/{item_id}",response_model=dsSensorHub.respSensors)         # Get Sensor Information
def getSensor(item_id: str | None = None):
    rtn=dsSensorHub.respSensor(id=item_id,description="Boiler Temp",type=1,value=0)
    return rtn

