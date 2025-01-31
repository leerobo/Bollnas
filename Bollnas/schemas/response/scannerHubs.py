from pydantic import BaseModel, Field

class Hubs(BaseModel):
    count: int        = Field(default=0,json_schema_extra={ 'description': 'Total Hubs'} ) 
    Hubs: list[dict]  = Field(default=None,json_schema_extra={ 'description': 'Hubs'} ) 

