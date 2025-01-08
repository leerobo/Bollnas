"""Define Response schemas specific to the Users."""

from pydantic import Field

from models.enums import RoleType
from schemas.base import UserBase
from schemas.examples import ExampleUser


class UserResponse(UserBase):
    """Response Schema for a User."""

    id: int = Field(ExampleUser.id)
    first_name: str = Field(examples=[ExampleUser.first_name])
    last_name: str = Field(examples=[ExampleUser.last_name])
    role: RoleType = Field(examples=[ExampleUser.role])
    banned: bool = Field(examples=[ExampleUser.banned])
    verified: bool = Field(examples=[ExampleUser.verified])


class MyUserResponse(UserBase):
    """Response for non-admin getting their own User data."""

    first_name: str = Field(examples=[ExampleUser.first_name])
    last_name: str = Field(examples=[ExampleUser.last_name])
