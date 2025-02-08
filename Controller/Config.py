"""Control the app settings, including reading from a .env file."""

from __future__ import annotations

import sys,os
from functools import lru_cache
from pathlib import Path  
from rich import print as rprint

from pydantic import field_validator,BaseModel,Field,ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from Common.Config.helpers import get_project_root

class Settings(BaseSettings):
    """Main Settings class.

    This allows to set some defaults, that can be overwritten from the .env
    file if it exists.
    Do NOT put passwords and similar in here, use the .env file instead, it will
    not be stored in the Git repository.
    """
    project_root: Path = get_project_root()
    api_root:str =""

    env_file: str = str(project_root / ".env")
    try:
      model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
    except Exception as e:
      rprint("[red]ERROR:   [/red][bold]Missing .env file")
      sys.exit(1)

    project_name:str = "The Bollnas Project"
    project_description:str ="""# The Bollnas Project
         Using Grafana and Prometheus to monitor RPIs dotted around the house was always a pain that you had to config prometheus with the APIs and Ports every time i added a RPI or the DNS hit the wall and everything has a different IP address.
         So now promethus just has access to the controller,  which is a set of APIs then force it to scan the LAN,  find sensorhubs,  registered them and them continue to poll them.  This allowed me to see realtime the RPIs status via the controllers Status API and uses the promethues Client repos to allow my main server to get the info and store it. 
         The sensorshub polls the sensors and relay pins and stores the settings ready for the next controller request,  it can also accept requests to toggle the relay pins via the controller. """

    cors_origins: str = "*"

    # Setup the Postgresql database.
    #db_user: str = "my_db_username"
    #db_password: str = "Sup3rS3cr3tP455w0rd"  # noqa: S105
    #db_address: str = "localhost"
    #db_port: str = "5432"
    #db_name: str = "api-template"

    # JTW secret Key
    secret_key: str = "1F24921CEADCE4E0113C84EFA60A9802"  # noqa: S105
    access_token_expire_minutes: int = 7200

    # Custom Metadata
    api_title: str = 'The Bollnas Project'
    api_description: str ="""Using Grafana and Prometheus to monitor RPIs dotted around the house was always a pain that you had to config prometheus with the APIs and Ports every time i added a RPI or the DNS hit the wall .
         So now promethus just has access to the controller,  which is a set of APIs that force it to scan the LAN,  find sensorhubs,  registered them and then continue to poll them.  

This allowed me to see realtime the RPIs status via the controllers Status API and uses the promethues Client repos to allow my main server to get the info and store it. 
         The sensorshub polls the sensors and relay pins and stores the settings ready for the next controller request,  
         it can also accept requests to toggle the relay pins via the controller. """

    repository: str = """ github : leerobo/bollnas """
    contact: dict[str, str] =  {"Author":"lee@ssshhhh.com"}
    #license_info: dict[str, str] = ['MIT']
    year: str = "2025"

    # Redis 
    redisTimer: int = 30              #  Sensors Valid in seconds
    redisHubTimer: int = 43200        #  Hub scanner valid for 12 hours (Use /Scan to force new Hub Scan when adding new Device)

    # Lan Scanner
    dns: str ="192.168.1.1"
    sensorHub_port: str ="14121"
    netgear_password: str = ""

    i_read_the_damn_docs: bool = False

    @field_validator("api_root")
    @classmethod
    def check_api_root(cls: type[Settings], value: str) -> str:
        """Ensure the api_root does not end with a slash."""
        if value and value.endswith("/"):
            return value[:-1]
        return value    
    
@lru_cache
def getConfig() -> Settings:
    """Return the current settings."""
    Settings.model_rebuild()
    return Settings()

