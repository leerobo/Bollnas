"""Control the app settings, including reading from a .env file."""

from __future__ import annotations

import sys,os
from functools import lru_cache
from pathlib import Path  
from rich import print as rprint

from pydantic import field_validator,BaseModel,Field,ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from Bollnas.config.helpers import get_project_root

class controllerType(BaseSettings):

    project_root: Path = get_project_root()
    env_file: str = str(project_root / ".envcontroller" )
    try:
      model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
    except Exception as e:
      rprint("[red]ERROR:   [/red][bold]Missing .env file")
      sys.exit(1)

    controller_name: str = Field(default="" )
    controller_description: str = Field(default="" )

class sensorhubType(BaseSettings):
    project_root: Path = get_project_root()
    env_file: str = str(project_root / ".envsensorhub" )
    try:
      model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
    except Exception as e:
      rprint("[red]ERROR:   [/red][bold]Missing .envsensorhub file")
      sys.exit(1)

    sensorhub_name: str = Field(default="" )
    sensorhub_location: str = Field(default="" )


class Settings(BaseSettings):
    """Main Settings class.

    This allows to set some defaults, that can be overwritten from the .env
    file if it exists.
    Do NOT put passwords and similar in here, use the .env file instead, it will
    not be stored in the Git repository.
    """
    project_root: Path = get_project_root()

    env_file: str = str(project_root / ".env")
    try:
      model_config = SettingsConfigDict(env_file=env_file,extra="allow",)
    except Exception as e:
      rprint("[red]ERROR:   [/red][bold]Missing .env file")
      sys.exit(1)

    base_url: str = "http://localhost:14120"
    api_root: str = ""
    no_root_route: bool = False

    cors_origins: str = "*"

    # Setup the Postgresql database.
    db_user: str = "my_db_username"
    db_password: str = "Sup3rS3cr3tP455w0rd"  # noqa: S105
    db_address: str = "localhost"
    db_port: str = "5432"
    db_name: str = "api-template"

    test_with_postgres: bool = False

    # Setup the TEST Postgresql database.
    test_db_user: str = "my_db_username"
    test_db_password: str = "Sup3rS3cr3tP455w0rd"  # noqa: S105
    test_db_address: str = "localhost"
    test_db_port: str = "5432"
    test_db_name: str = "api-template-test"

    # JTW secret Key
    secret_key: str = "1F24921CEADCE4E0113C84EFA60A9802"  # noqa: S105
    access_token_expire_minutes: int = 7200

    # Custom Metadata
    api_title: str = 'The Bollnas Project'
    api_description: str = """ RPI controller and Sensor Hub Fast API  """
    repository: str = """ github : leerobo/bollnas """
    contact: dict[str, str] =  {"Author":"lee@ssshhhh.com"}
    #license_info: dict[str, str] = ['MIT']
    year: str = "2025"

    # email settings
    mail_username: str = "test_username"
    mail_password: str = "s3cr3tma1lp@ssw0rd"  # noqa: S105
    mail_from: str = "test@email.com"
    mail_port: int = 587
    mail_server: str = "mail.server.com"
    mail_from_name: str = "The Bollnas Project"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    mail_use_credentials: bool = True
    mail_validate_certs: bool = True

    # Controller & sensorhub set defaults
    load_controller: bool=False
    load_sensorhub: bool=False

    dns: str ="192.168.1.1"
    sensorHub_port: str ="14121"
    controller_port: str ="14120"
    netgear_password: str = ""

    project_description: str = ""


    # controller_settings: Optional[controllerType] = Field(default=None)
    # sensorhub_settings: Optional[sensorhubType]  = Field(default=sensorhubType )

    # gatekeeper settings!
    # this is to ensure that people read the damn instructions and changelogs
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

@lru_cache
def get_controller_settings() -> controllerType:
    """Return the current settings."""
    controllerType.model_rebuild()
    return controllerType()

@lru_cache
def get_sensorhub_settings() -> sensorhubType:
    """Return the current settings."""
    sensorhubType.model_rebuild()
    return sensorhubType()
 