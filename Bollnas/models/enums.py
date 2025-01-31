# pylint: disable=invalid-name
"""Define Enums for this project."""

from enum import Enum


class RoleType(Enum):
    """Contains the different Role types Users can have."""

    user = "user"
    admin = "admin"

class DeviceType(Enum):
    """Device Types"""

    controller = "Controller"
    sensorhub = "SensorHub"    
    unknown = "Unknown"   

class SensorType(Enum):
    """Supported Sensor Types"""

    DS18B20  = "DS18B20"
    relay    = "Relay"    
    unknown  = "Unknown"   

class SensorPlatform(Enum):
    """Supported Sensor Platform """

    wire1    = "wire-1"
    zigbee   = "zigbee"    
    mater    = "mater"    
    unknown  = "Unknown"   

class SensorMeasurement(Enum):
    """Supported Sensor Measurements """

    c        = "Celsius"
    f        = "Fahrenheit"    
    kelvin   = "Kelvin"    
    percent  = "Percentage"       
    number   = "Number"