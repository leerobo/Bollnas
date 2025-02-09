"""Define the Cached model."""

from pydantic import BaseModel, ConfigDict, Field
import datetime

class Sensor(BaseModel):
    name: str
    id: str  
    description: str 
    type: int 
    value: int 

class Sensorhub(BaseModel):
    name: str
    mac: str
    ip: str
    sensors: list[Sensor] 

class Controller(BaseModel):
    name: str 
    timestamp: str = Field(default_factory=datetime.datetime.now().isoformat)
    hubs: list[Sensorhub]

