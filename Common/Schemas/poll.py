from pydantic import BaseModel, Field
# import Common.Models.enums as enums
from Common.Schemas.Sensors import wire1, gpio

### Built by sensorHubs and processed by Controllers

class Poll(BaseModel):
    timestamp: str                     = Field(default=None,json_schema_extra={ 'description': 'Sensor Poll TimeStamp'} ) 
    wire1Sensors: list[wire1.Status]   = Field(default=[],json_schema_extra={ 'description': 'Wire 1 Sensors'} ) 
    GPIOsettings: list[gpio.Pins]      = Field(default=[],json_schema_extra={ 'description': 'GPIO status'} ) 


class FullPoll(BaseModel):
    timestamp: str                     = Field(default=None,json_schema_extra={ 'description': 'Sensor Poll TimeStamp'} ) 
    polls: dict                        = Field(default=None,json_schema_extra={ 'description': 'SensorHub Poll'} ) 

 