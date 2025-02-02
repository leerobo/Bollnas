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

    print('root',project_root)
    env_file: str = str(project_root / ".env")
    try:
      model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
    except Exception as e:
      rprint("[red]ERROR:   [/red][bold]Missing .env file")
      sys.exit(1)

    project_name:str = "The Bollnas Project"
    project_description:str ="# The Bollnas Project"

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
    api_description: str = """ RPI controller API  """
    repository: str = """ github : leerobo/bollnas """
    contact: dict[str, str] =  {"Author":"lee@ssshhhh.com"}
    #license_info: dict[str, str] = ['MIT']
    year: str = "2025"

    # Lan Scanner
    dns: str ="192.168.1.1"
    sensorHub_port: str ="14121"
    netgear_password: str = ""

    # Wire1 Directory 
    wire1Dir: str = "/sys/bus/w1/devices/"

    # relays BCD
    GPIOrelays: list[int] = [12,16,20,21]

    i_read_the_damn_docs: bool = False

    @field_validator("api_root")
    @classmethod
    def check_api_root(cls: type[Settings], value: str) -> str:
        """Ensure the api_root does not end with a slash."""
        if value and value.endswith("/"):
            return value[:-1]
        return value    
    
@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    Settings.model_rebuild()
    return Settings()

