from pydantic import BaseModel, Field
import Common.Models.enums as enums

class Status(BaseModel):
    id: str
    description:str                       = Field(default=None,json_schema_extra={ 'description': 'Sensor Description'} ) 
    value: float                          = Field(default=-81,json_schema_extra={ 'description': 'Sensor Value'} ) 
    type: enums.SensorType                = Field(default=enums.SensorType.unknown,json_schema_extra={ 'description': 'Sensor Type'} ) 
    measurement: enums.SensorMeasurement  = Field(default=enums.SensorMeasurement.number,json_schema_extra={ 'description': 'Sensor Value Measurement Type'} ) 
    platform: enums.SensorPlatform        = Field(default=enums.SensorPlatform.unknown,json_schema_extra={ 'description': 'Sensor Platform'} ) 
    description: str                      = Field(default='',json_schema_extra={ 'description': 'Sensor Description'} ) 
