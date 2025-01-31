
from pydantic import BaseModel

class Ping(BaseModel):
    name: str
    description: str | None = None
    attached: int | None = 0
    devices:  list[dict] | None = [{"Message":"None Attached"}]

 