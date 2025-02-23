"""Control the app settings, including reading from a .env file."""

from __future__ import annotations

import sys,os
from typing import Dict, Any

from functools import lru_cache
from pathlib import Path  
from rich import print as rprint

from pydantic import field_validator,BaseModel,Field,ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from Common.helpers import get_project_root
import Common.Models.enums as enums

 
class Settings(BaseSettings):
    """Main Settings class.

    This allows to set some defaults, that can be overwritten from the .env
    file if it exists.
    Do NOT put passwords and similar in here, use the .env file instead, it will
    not be stored in the Git repository.
       
    """
    project_root: Path = get_project_root()
    api_root:str =""
    
    if os.getenv("CONTROLLER") == 'True' :
      try:
        env_file: str = str(project_root / "Controller/controller.env")
        model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
        rprint("[orange3]CNTL:     [/orange3][bold]Loaded controller.env BluePrint")
      except Exception as e:
        rprint("[red]ERROR:     [/red][bold]Missing SensorHub .env file")
        sys.exit(1)

    if os.getenv("SENSORHUB") == 'True':
      try:
        env_file: str = str(project_root / "SensorHub/sensorhub.env")
        model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
        rprint("[orange3]CNTL:     [/orange3][bold]Loaded SensorHub.env BluePrint")
      except Exception as e:
        rprint("[red]ERROR:     [/red][bold]Missing SensorHub .env file")
        sys.exit(1)

    project_name:str = "The Bollnas Project"
    project_description:str ="""# The Bollnas Project
         Using Grafana and Prometheus to monitor RPIs dotted around the house was always a pain that you had to config prometheus with the APIs and Ports every time i added a RPI or the DNS hit the wall and everything has a different IP address.
         So now promethus just has access to the controller,  which is a set of APIs then force it to scan the LAN,  find sensorhubs,  registered them and them continue to poll them.  This allowed me to see realtime the RPIs status via the controllers Status API and uses the promethues Client repos to allow my main server to get the info and store it. 
         The sensorshub polls the sensors and relay pins and stores the settings ready for the next controller request,  it can also accept requests to toggle the relay pins via the controller. """

    cors_origins: str = "*"

    # Custom Metadata
    api_title: str = 'The Bollnas Project'
    api_description: str =""" """
    api_location: str = ""
    repository: str = """ github : leerobo/bollnas """
    contact: dict[str, str] =  {"Author":"lee@ssshhhh.com"}
    year: str = "2025"

    # Redis 
    redisTimer: int = 30              #  Sensors Valid in seconds
    redisHubTimer: int = 43200        #  Hub scanner valid for 12 hours (Use /Scan to force new Hub Scan when adding new Device)

    # Lan Scanner 
    dns: str ="192.168.1.1"
    sensorHub_port: str ="14121"
    netgear_password: str = ""

    # Security covers all LAN local devices between Controller and SensorHubs
    # keys and Certs are LAN based and are used if the security flag is True
    # its advisable to place Cert outside of the code in a more secure folder on the device
    #   If true then apiKey or PEM,  
    #      PEM can be a genric self signed Cert private and public keys.
    #      apiKey is a UUID        
    #   
    security: bool = False
    securityKey: enums.SecurityLevel = enums.SecurityLevel.off
    key: str  =  ""
    pem: str  =  "/cert/jwt.pem"

    # Wire1 Directory 
    wire1: bool = True
    wire1dir: str = "/sys/bus/w1/devices/"
    wire1description: dict[str, str]  =  {}

    # relays BCD
    relays: bool = True
    GPIOrelays: list[int] = [26]
    GPIOdescription: dict[str, str] =  {}

   # Zigbee
    zigbee: bool = False

    i_read_the_damn_docs: bool = False

    @field_validator("wire1description","GPIOdescription")
    @classmethod
    def w1d(cls: type[Settings], value: str) -> str:
        return value    
    
@lru_cache
def getConfig() -> Settings:
    """Return the current settings."""
    Settings.model_rebuild()
    return Settings()

