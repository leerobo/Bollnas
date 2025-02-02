from pydantic import BaseModel, Field, ConfigDict
import Bollnas.models.enums as enums

class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str 

