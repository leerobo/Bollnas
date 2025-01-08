from pydantic import BaseModel

class Sensor(BaseModel):
    id: str
    description: str | None = None
    type: int | None = None
    value: int | None = None

class Sensors(BaseModel):
    count: int | None = 0
    sensors: list[Sensor] | None = None

 