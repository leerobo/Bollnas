from pydantic import BaseModel, Field,ConfigDict
import Common.Models.enums as enums

### Used by Controllers to hold sensorHub Details 

class CustomBaseModel(BaseModel):
    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.model_fields.keys(), tpl)})
    
class Hub(CustomBaseModel):
    model_config                   = ConfigDict(extra="allow")
    name: str                      = Field(default=None,json_schema_extra={ 'description':'Name'})
    ip: str                        = Field(json_schema_extra={ 'description':'IP' })
    mac: str                       = Field(default=None,json_schema_extra={ 'description':'Mac'})
    type: str                      = Field(default=None,json_schema_extra={ 'description':'Type'})
    security: bool                 = Field(default=False,json_schema_extra={ 'description':'Secure'})

class Hubs(BaseModel):
    count: int              = Field(default=0,json_schema_extra={ 'description': 'Total Hubs'} ) 
    SensorHubs: list[Hub]   = Field(default=None,json_schema_extra={ 'description': 'Hubs'} ) 

