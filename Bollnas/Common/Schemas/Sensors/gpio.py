from pydantic import BaseModel, Field
import Common.Models.enums as enums
from typing import Optional

class Pins(BaseModel):
    pin: int                           = Field(default=None,json_schema_extra={ 'description': 'GPIO BCD pin number'} ) 
    pintype: enums.GPIOdeviceAttached  = Field(default=enums.GPIOdeviceAttached.unknown,json_schema_extra={ 'description': 'GPIO Attached'} ) 
    status: enums.GPIOstatus           = Field(default=enums.GPIOstatus.unknown,json_schema_extra={ 'description': 'GPIO Status'} )  
    value: float                       = Field(default=-83,json_schema_extra={ 'description': 'GPIO pwm Value'} ) 
    direction: enums.GPIOdirection     = Field(default=enums.GPIOdirection.out,json_schema_extra={ 'description': 'GPIO Pin Direction'} ) 
    description: str                   = Field(default='',json_schema_extra={ 'description': 'GPIO Description'} ) 
    reason: str                        = Field(default=None,json_schema_extra={ 'description': 'GPIO Generic Reason'} ) 

class PinChange(BaseModel):
    pin: int                           = Field(default=None,json_schema_extra={ 'description': 'GPIO BCD pin number'} ) 
    task : enums.GPIOtask              = Field(default=enums.GPIOtask.toggle,json_schema_extra={ 'description': 'GPIO Task'} ) 
    status: enums.GPIOstatus           = Field(default=enums.GPIOstatus.unknown,json_schema_extra={ 'description': 'GPIO Status'} )  
    value : float                      = Field(default=None,json_schema_extra={ 'description': 'GPIO Task result'} ) 
    reason: str                        = Field(default='',json_schema_extra={ 'description': 'GPIO Generic Reason'} ) 
