from pydantic import BaseModel 

class Headers(BaseModel):
    model_config = {"extra": "allow"}
    x_apikey: str | None  = None
