"""Define routes for Authentication."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
# from Bollnas.managers.auth import AuthManager
# from Bollnas.managers.user import UserManager
from Bollnas.schemas.response import sensor_hubs

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["Controller"])

@router.get("/scan",status_code=status.HTTP_200_OK,
    name="Scan Lan for SensorHubs",
    response_model=sensor_hubs.SensorHubs
)
def scan():
    print('----- Scanning')
    ip_range = '192.168.1.0/24'
    print('----- end')
    return {'status': 'ok'}