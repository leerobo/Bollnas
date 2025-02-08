from pydantic import BaseModel, Field
import Common.Models.enums as enums
import Sensors. as 
import Sensors.wire1 as wire1

### Built by sensorHubs and processed by Controllers

class Ping(BaseModel):
    name: str
    description: str                      = Field(default=None,json_schema_extra={ 'description': 'SensorHub Description'} ) 
    devicetype: enums.DeviceType          = Field(default=enums.DeviceType.unknown,json_schema_extra={ 'description': 'Sensor Value'} )  
    wire1:  bool                          = Field(default=False,json_schema_extra={ 'description': 'Wire1 Presents'} ) 
    relays: bool                          = Field(default=False,json_schema_extra={ 'description': 'Relay Present'} ) 
