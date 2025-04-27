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

class ControllerSettings(BaseSettings,extra="allow"):
    model_config = SettingsConfigDict(env_file="/home/lero/Github/Home/Bollnas/Bollnas/Controller/controller.env")
    dns: str ="192.168.2.1"
    sensorHub_port: str ="14121"
    netgear_password: str = ""
    pihole_password:  str = ""
    static_sensorhubs: list =  []

class SensorHubSettings(BaseSettings,extra="allow" ):
    model_config = SettingsConfigDict(env_file="/home/lero/Github/Home/Bollnas/Bollnas/SensorHub/sensorhub.env")

    security: bool = False
    securityKey: enums.SecurityLevel = enums.SecurityLevel.off
    key: str  =  ""
    pem: str  =  "/cert/jwt.pem"

    # Wire1 Directory 
    wire1: bool = True
    wire1dir: str = "/sys/bus/w1/devices/"
    wire1description: dict[str, str]  =  {}

    # relays BCD
    relays: bool = False
    GPIOrelays: list[int] = []
    GPIOdescription: dict[str, str] =  {}

   # Zigbee
    zigbee: bool = False

    @field_validator("wire1description","GPIOdescription")
    @classmethod
    def w1d(cls: type[DefaultSettings], value: str) -> str:
        return value   
 
class DefaultSettings(BaseSettings):
    """Main Settings class.
      This allows to set some defaults, that can be overwritten from the .env
      file if it exists.
      Do NOT put passwords and similar in 
      here, use the .env file instead, it will
      not be stored in the Git repository.
    """
    project_root: Path = get_project_root()
    api_root:str =""
    print(os.getenv("CONTROLLER"),'-',os.getenv("SENSORHUB"),'--',get_project_root())

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

    # Metric Labels 
    metric_required:    bool = True          # True if promethueus Metrics Required
    # Prometheus Fullname Location_deviceName_<Sensor name>
    metric_controllerName:    str  = 'stockholm'   # controller name 
    metric_sensorHubName:     str  = 'garage'      # Sensorhub name 

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

    i_read_the_damn_docs: bool = False


#@lru_cache
def getConfig() -> DefaultSettings:
    """ Return A Config Field """
    DefaultSettings.model_rebuild()
    return DefaultSettings()

#@lru_cache
def getControllerConfig() -> ControllerSettings:
    """Return the Controller Settings."""
    ControllerSettings.model_rebuild()
    return ControllerSettings()

#@lru_cache
def getSensorHubrConfig() -> SensorHubSettings:
    """Return the SensorHub settings."""
    SensorHubSettings.model_rebuild()
    return SensorHubSettings()

 