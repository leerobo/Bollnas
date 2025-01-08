"""Define routes for Authentication."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
from Bollnas.managers.auth import AuthManager
from Bollnas.managers.user import UserManager
from Bollnas.schemas.response.ping import Ping

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["Controller"])

@router.post("/info",status_code=status.HTTP_200_OK,
    name="Ping SensonHub",
    response_model=Ping
)
def ping():
    return Ping(name="Hub",description="Boiler",attached=0,devices=[{"Message":"None Attached"}])
