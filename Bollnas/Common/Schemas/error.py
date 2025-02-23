from pydantic import BaseModel, Field, ConfigDict
import Common.Models.enums as enums

class response(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str 

