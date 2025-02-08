#!/usr/bin python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Gauge
from urllib import parse
import RPi.GPIO as GPIO
import configparser 
import time
import http.client
import json

import sys
import os
import time
import datetime
import glob
import socket
from array import array
#from systemd import journal
#import Adafruit_DHT
import logging
import socketserver
from typing import Union

from  SensorHub.ConfigSensorhub.settings import get_settings
import Common.Schemas.response.sensors as Schema
from Common.Schemas.response.gpio import GPIOresponse
from Common.Schemas.request.gpio import GPIOrequest
import Common.Models.enums as enums

from rich import print as rprint

# configPOLL = configparser.ConfigParser()
# configPINS = configparser.ConfigParser()
# KillSwitch = True
# POLLlst={"DEF":0}
# GaugeW1={"DEF":20}   # W1 Sensors
# GaugePIN={"DEF":20}  # Activate Pins
# Vers='1.0.2'
# MID='XX'
# #global PortNo
# #global POLLgap

async def poll(): 
    rtn={}
    rtn['timestamp']=str(datetime.datetime.now())
    rtn['wire1Sensors']=pollWire1()
    rtn['GPIOsettings']=pollGPIO()
    rprint('Poll :',rtn)    
    return rtn
          
# ---------------- WIRE 1 find and read --------------------

def pollWire1() -> list[Schema.Sensor]:
    """ ## Wire 1 Poll
    On RPI on sensors Wire-1 connects are held in the wireDir1 directory,
    This scans the Directory for the files,  one file, one sensor.
    """
    wire1Sensors=[]
    SIDs=[]
    devicelist = glob.glob(get_settings().wire1Dir+'28*')   #  DS18 Sensors

    if devicelist!='':
        for device in devicelist:
            TT=device.split("/")
            SID = TT[len(TT)-1]
            sensorVal=readWire1(SID)
            if sensorVal > -999:
               wire1Sensors.append( Schema.Sensor(id='W1_S'+SID[3:], 
                                 type=enums.SensorType.DS18B20, 
                                 measurement=enums.SensorMeasurement.c, 
                                 platform=enums.SensorPlatform.wire1, 
                                 value=sensorVal,
                                 description=getDescriptions('W1_S'+SID[3:])
                                 )  )

    return wire1Sensors
def readWire1(SID) -> float:
    """ Read Wire 1 sensors from Directory based on Sensor ID(File name) """
    devicefile=get_settings().wire1Dir+SID+'/w1_slave'
    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    
        if lines[0][-4:-1] =="YES":            # Check Status Code 
          equals_pos = lines[1].find('t=')   # Get value from 2nd Line
          temp_string = lines[1][equals_pos+2:]
          return float(temp_string)/1000
        
        rprint('[yellow]Sensor {} status is {} invalid'.format(SID,lines[0][-4:-1]) )
        return -999
    except Exception as ex:
        rprint('[red]Sensor {} Read Error : {}'.format(SID,ex) )
        return -999

# ---------------- GPIO Pin Reads --------------------

# Return Pin ON/OFF status
def pollGPIO()  -> list[GPIOresponse]:
    rprint('[yellow]GPIO Scanning')
    rtn=[]
    try:
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        for relay in get_settings().GPIOrelays:
            # GPIO.setup(int(relay), GPIO.OUT)
            rtn.append( GPIOread( GPIOresponse(pin=relay,pintype=enums.GPIOdeviceAttached.relay,direction=enums.GPIOdirection.out)  ) )
    except Exception as ex:
        rprint('[red]Sensor {} Read Error : {}'.format(relay,ex) )
        rtn.append( GPIOread( GPIOresponse(pin=relay,pintype=enums.GPIOdeviceAttached.relay,
                                           direction=enums.GPIOdirection.out,
                                           status=enums.GPIOstatus.error,value=-86,
                                           description=getDescriptions(relay)
                                           )  )  )
    return rtn
def getDescriptions(pinW1) -> str:
    print(pinW1,get_settings().GPIOdescription)
    if str(pinW1) in get_settings().GPIOdescription:  return get_settings().GPIOdescription[str(pinW1)]
    if str(pinW1) in get_settings().WIRE1description: return get_settings().WIRE1description[str(pinW1)]
    return ""

# Control GPIO Pins 
def GPIOread(pin: GPIOresponse) -> GPIOresponse:
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin.pin, GPIO.OUT)
    try:
       pin.value = GPIO.input(pin.pin)
       pin.status = enums.GPIOstatus.ok
       return pin
    except Exception as ex:
       rprint('[red]GPIO Read Error ',pin.pin,':',ex)
       pin.value = -85
       pin.status = enums.GPIOstatus.error
       return pin
def GPIOset(pinReq:GPIOresponse,task:enums.GPIOtask) -> GPIOresponse:
    currentPin=GPIOread(pinReq)
    if currentPin.status != enums.GPIOstatus.ok:      return currentPin 
    GPIO.setup(pinReq.pin, GPIO.OUT)
    try:
       if   task == enums.GPIOtask.toggle and currentPin.value == 0 :
                GPIO.output(pinReq.pin, 1)
       elif task == enums.GPIOtask.toggle and currentPin.value == 1 :
                GPIO.output(pinReq.pin, 0)
       elif task == enums.GPIOtask.on :
                GPIO.output(pinReq.pin, 0)
       else :   GPIO.output(pinReq.pin, 1)
       return  GPIOread(pinReq)
    
    except Exception as ex:
        rprint('[red]Sensor {} Set Error : {}'.format(pinReq,ex) )
        currentPin.status=enums.GPIOstatus.error
        currentPin.value=-86
        return currentPin

def GPIOcontrol(pin):
    rprint('[yellow]GPIO Control')
    try:
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        rprint('[yellow]Relay {} Status {}'.format(pin,GPIO.input(int(pin))) )

        return -999
    except Exception as ex:
        rprint('[red]Sensor {} Read Error : {}'.format(pin,ex) )
        return -999         

    # GPIO.setwarnings(False) 
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(int(PIN), GPIO.OUT)
    # if GPIO.input(int(PIN)):
    #     return 1  
    # else:
    #     return 0   
    # sys.stdout.flush()
