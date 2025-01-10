"""Define routes for Authentication."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
# from Bollnas.managers.auth import AuthManager
# from Bollnas.managers.user import UserManager
from Bollnas.schemas.response.ping import Ping

from rich import print as rprint
from Bollnas.config.settings import get_settings

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["Controller"])

@router.get("/info",status_code=status.HTTP_200_OK,
    name="Ping SensonHub",
    response_model=Ping
)
def ping():
    return Ping(name=get_settings().api_title, description=get_settings().api_description, attached=0,devices=[{"Message":"None Attached"}])
