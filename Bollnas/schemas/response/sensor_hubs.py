from pydantic import BaseModel

class SensorHubs(BaseModel):
    count: int | None = 0
    Hubs: list[dict] | None = None

