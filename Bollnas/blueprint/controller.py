"""Define routes for Authentication."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Bollnas.database.db import get_database
# from Bollnas.managers.auth import AuthManager
# from Bollnas.managers.user import UserManager
from Bollnas.schemas.response import sensor_hubs

from Bollnas.managers.scanner import scan_lan

#from schemas.request.user import UserLoginRequest, UserRegisterRequest
#from schemas.response.auth import TokenRefreshResponse, TokenResponse

router = APIRouter(tags=["Controller"])

@router.get("/scan",status_code=status.HTTP_200_OK,
    name="Scan Lan for SensorHubs",
    response_model=sensor_hubs.SensorHubs
)
def scan_hubs():
    devices = scan_lan()
    for device in devices:
       print(f"IP: {device['ip']}, MAC: {device['mac']}")
    return sensor_hubs.SensorHubs(count=len(devices),Hubs=list(devices))
    # TODO: store hubs to a generic thread safe area 
