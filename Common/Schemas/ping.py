from pydantic import BaseModel, Field
import Common.Models.enums as enums

### Built by sensorHubs and processed by Controllers

class PingResponse(BaseModel):
    name: str
    description: str                      = Field(default=None,json_schema_extra={ 'description': 'SensorHub Description'} ) 
    devicetype: enums.DeviceType          = Field(default=enums.DeviceType.unknown,json_schema_extra={ 'description': 'Sensor Value'} )  
    security: bool                        = Field(default=False,json_schema_extra={ 'description': 'Secure'} ) 
    securityKey: enums.SecurityLevel      = Field(default=enums.SecurityLevel.off,json_schema_extra={ 'description': 'Security Level'} ) 
    wire1:  bool                          = Field(default=False,json_schema_extra={ 'description': 'Wire1 Presents'} ) 
    relays: bool                          = Field(default=False,json_schema_extra={ 'description': 'Relay Present'} ) 
    zigbee: bool                          = Field(default=False,json_schema_extra={ 'description': 'Zigbee Hat Present'} ) 