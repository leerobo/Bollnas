"""Control the app settings, including reading from a .env file."""

from __future__ import annotations

import sys,os,json,re
from typing import Dict, Any

from functools import lru_cache
from pathlib import Path  
from rich import print as rprint

from pydantic import field_validator,BaseModel,Field,ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from Common.helpers import get_project_root
import Common.Models.enums as enums

class TheInstallation(BaseSettings,extra="allow"):
    Location: str 
    Room: str 
    Software_Version: str = "0.0.1" 
    Release_Date: str     = "2024-09-25"
    Install_Date: str     = "2024-09-25"

class TheSensorHubs(BaseSettings,extra="allow"):
    Wire1dir: str    = "/sys/bus/w1/devices/"
    Wire1: bool      = False
    Zigbee: bool     = False
    Sensors: list[dict[str, str]] = {}
    Relays: list[dict[str, str]] = {}


class TheController(BaseSettings,extra="allow"):
    dns : str   =  Field(default="192.168.1.1")
    Port_Scanner : int  = 14121
    Netgear_Pwd : str   =  ""  
    piHole_Pwd  : str   =  ""                     
    Static_Sensorhubs : list[str] =  [] 

class TheSecurity(BaseSettings,extra="allow"):
    Comms : bool = False
    apikey : str = ""
    pemCert : str = ""

class TheCache(BaseSettings,extra="allow"):
    Timer : int = 30 
    HubTimer : int = 43200
    host : str = "localhost"
    port : int = 6379
    db : int = 0

# ------------------------------------------------------------------

class Settings(BaseSettings,extra="allow"):
    Title: str       = "The Bollnas Project"
    Description: str = "Sensor Hub for Main Boiler"
    metric_required: bool = False 
    cors_origins : str =  "*"

    Installation:  TheInstallation 
    ControllerHub: TheController
    SensorHubs:    TheSensorHubs
    Security:      TheSecurity
    Cache:         TheCache

# ------------------------------------------------------------------ 

#@lru_cache
def getJSONconfig() -> Settings:
    with open(get_project_root() / 'Config.json', 'r') as file:
        # data = json.loads(re.sub("//.*","",file,flags=re.MULTILINE))
        data = json.load(file)
    try:
       Config=Settings(**data)
    except Exception as e:
       rprint(f'[red]ERROR:   [/red] {e}')
       sys.exit(1)

    return Config

 