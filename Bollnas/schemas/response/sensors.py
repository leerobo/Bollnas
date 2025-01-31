from pydantic import BaseModel, Field
import Bollnas.models.enums as enums

class Sensor(BaseModel):
    id: str
    description:str                       = Field(default=None,json_schema_extra={ 'description': 'Sensor Description'} ) 
    value: float                          = Field(default=None,json_schema_extra={ 'description': 'Sensor Value'} ) 
    type: enums.SensorType                = Field(default=enums.SensorType.unknown,json_schema_extra={ 'description': 'Sensor Type'} ) 
    measurement: enums.SensorMeasurement  = Field(default=enums.SensorMeasurement.number,json_schema_extra={ 'description': 'Sensor Value Measurement Type'} ) 
    platform: enums.SensorPlatform        = Field(default=enums.SensorPlatform.unknown,json_schema_extra={ 'description': 'Sensor Platform'} ) 

class Sensors(BaseModel):
    count: int                            = Field(default=0,json_schema_extra={ 'description': 'Attached Sensors'} ) 
    sensors: list[Sensor]                 = Field(default=None,json_schema_extra={ 'description': 'Sensors'} ) 

class Ping(BaseModel):
    name: str
    description: str                      = Field(default=None,json_schema_extra={ 'description': 'SensorHub Description'} ) 
    devicetype: enums.DeviceType          = Field(default=enums.DeviceType.unknown,json_schema_extra={ 'description': 'Sensor Value'} )  
    devices:  Sensors                     = Field(default=None,json_schema_extra={ 'description': 'Sensors'} ) 
