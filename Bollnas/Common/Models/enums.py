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

# Pin controllers

class GPIOdirection(Enum):
    """ GPIO Direction """
    inn      = "inn"
    out      = "out"    
    pwm      = 'pwm'

class GPIOdeviceAttached(Enum):
    """ GPIO Attached Device """
    unknown  = "unknown"
    relay    = "relay"

class GPIOstatus(Enum):
    """ GPIO polling Status """
    error    = "inError"
    ok       = "ok"
    unknown  = "unknown"

class GPIOtask(Enum):
    """ GPIO Task """
    read        = "read"
    toggle      = "toggle"
    on          = "on"   
    off         = "off"   

# Security
class SecurityLevel(Enum):
    off            = "off"  
    apiKey         = "apiKey"  
    jwt            = "jwt"  
    password       = "**pa$$word**"  
    