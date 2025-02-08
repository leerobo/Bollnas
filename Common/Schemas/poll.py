from pydantic import BaseModel, Field
# import Common.Models.enums as enums
from Common.Schemas.Sensors import wire1, gpio

### Built by sensorHubs and processed by Controllers

class Poll(BaseModel):
    timestamp: str                     = Field(default=None,json_schema_extra={ 'description': 'Sensor Poll TimeStamp'} ) 
    wire1Sensors: list[wire1.Status]   = Field(default=[],json_schema_extra={ 'description': 'Wire 1 Sensors'} ) 
    GPIOsettings: list[gpio.Pins]      = Field(default=[],json_schema_extra={ 'description': 'GPIO status'} ) 

# class Sensor(BaseModel):              <<<< replaced by wire1Sensor
#     id: str
#     description:str                       = Field(default=None,json_schema_extra={ 'description': 'Sensor Description'} ) 
#     value: float                          = Field(default=None,json_schema_extra={ 'description': 'Sensor Value'} ) 
#     type: enums.SensorType                = Field(default=enums.SensorType.unknown,json_schema_extra={ 'description': 'Sensor Type'} ) 
#     measurement: enums.SensorMeasurement  = Field(default=enums.SensorMeasurement.number,json_schema_extra={ 'description': 'Sensor Value Measurement Type'} ) 
#     platform: enums.SensorPlatform        = Field(default=enums.SensorPlatform.unknown,json_schema_extra={ 'description': 'Sensor Platform'} ) 

# class Sensors(BaseModel):
#     count: int                            = Field(default=0,json_schema_extra={ 'description': 'Attached Sensors'} ) 
#     sensors: list[Sensor]                 = Field(default=None,json_schema_extra={ 'description': 'Sensors'} ) 
 