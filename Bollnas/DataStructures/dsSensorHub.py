from pydantic import BaseModel

class respPing(BaseModel):
    name: str
    description: str | None = None
    attached: int | None = 0
    devices:  list[dict] | None = [{"Message":"None Attached"}]

class respSensor(BaseModel):
    id: str
    description: str | None = None
    type: int | None = None
    value: int | None = None
    
class respSensors(BaseModel):
    count: int | None = 0
    sensors: list[respSensor] | None = None

