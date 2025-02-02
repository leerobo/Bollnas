"""Define Schemas used by the User routes."""

from pydantic import BaseModel,  Field
import Bollnas.models.enums as enums

class GPIOrequest(BaseModel):
    """Request schema for the Register Route."""
    pin: int              = Field(description='Pin to control')
    task: enums.GPIOtask  = Field(description='Task on Pin')



