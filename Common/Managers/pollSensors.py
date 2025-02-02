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

from Bollnas.config.settings import get_settings,get_sensorhub_settings
import Bollnas.schemas.response.sensors as Schema
from Bollnas.schemas.response.gpio import GPIOresponse
from Bollnas.schemas.request.gpio import GPIOrequest
import Bollnas.models.enums as enums

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
                                 value=sensorVal) 
                                 )

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
        rtn.append( GPIOread( GPIOresponse(pin=relay,pintype=enums.GPIOdeviceAttached.relay,direction=enums.GPIOdirection.out,
                                           status=enums.GPIOstatus.error,value=-86
                                           )  ) )
    return rtn


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

# # set Pin
# def RelaySET(PIN,tsk):
#     GPIO.setwarnings(False) 
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(int(PIN), GPIO.OUT)
#     if tsk=='ON':
#        GPIO.output(int(PIN), GPIO.LOW)
#        return "0"
#     else:
#        GPIO.output(int(PIN), GPIO.HIGH)
#        return "1"        
#     sys.stdout.flush()  

# # Toggle Pin
# def RelayTOGGLE(PIN):
#     GPIO.setwarnings(False) 
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(int(PIN), GPIO.OUT)
#     if RelayGET(PIN):
#        GPIO.output(int(PIN), GPIO.LOW)
#        return "0"
#     else:
#        GPIO.output(int(PIN), GPIO.HIGH)
#        return "1"        
#     sys.stdout.flush()  

# ---------------- GPIO Pin Reads --------------------


# def DelPromethues(typ,key):
#     global GaugePIN
#     global GaugeW1
#     Mkey = MID + '_' + key
#     SendMSG('DEL:'+Mkey+' - '+typ+' - '+key )    
#     if typ=='W1' and key in GaugeW1:
#         GaugeW1.pop(key)
#     elif  typ=='PIN' and key in GaugePIN:
#         GaugePIN.pop(key)

# def UpdPromethues(typ,key,val):
#     global GaugePIN
#     global GaugeW1
#     Mkey = MID + '_' + key
#     if not isSetPromethues(typ,key):
#         AddPromethues(typ,key)
#         SendMSG('New '+typ+' Allocation : '+key)

#     #SendMSG('UPD:'+Mkey+' - '+typ+' - '+key+' = '+str(val) )    
#     if typ=='W1' and key in GaugeW1:
#         GaugeW1[key].set(val)
#     elif  typ=='PIN' and key in GaugePIN:
#         GaugePIN[key].set(val)

# def AddPromethues(typ,key):
#     global GaugePIN
#     global GaugeW1
#     Mkey = MID + '_' + key
#     SendMSG('ADD:'+Mkey+' - '+typ+' - '+key)
#     if  typ == 'W1' and not key in GaugeW1:
#         GaugeW1[key]=Gauge(Mkey,key)
#     elif typ == 'PIN' and not key in GaugePIN:
#         GaugePIN[key]=Gauge(Mkey,key)
            
# def isSetPromethues(typ,key):
#     Mkey = MID + '_' + key
#     if typ == 'W1' and not key in GaugeW1:
#         return False
#     elif typ == 'PIN' and not key in GaugePIN:
#         return False
#     else:
#         return True

# def ValidatePARMS():
#     configPOLL.read('POLL.ini')
#     configPINS.read('PINS.ini')
#     if "location" not in configPOLL["POLL"]:
#         SendMSG('location missing from Config - Job Terminated')
#         return False
#     if "name" not in configPOLL["POLL"]:
#         SendMSG('name missing from Config - Job Terminated')
#         return False
#     return True    

# def SendMSG(msg):
#     print(msg)
#     #journal.send(msg)   

# def ReportPARMS():
#     global MID
#     global PortNo
#     global POLLgap
#     print("Location     : ",configPOLL["POLL"]["location"])
#     print("Name         : ",configPOLL["POLL"]["name"])
#     SendMSG(configPOLL["POLL"]["name"]+' / '+configPOLL["POLL"]["name"])
#     MID=configPOLL["POLL"]["location"]+'_'+configPOLL["POLL"]["name"]+'_V2'
#     SendMSG('Promethues Prefix : '+MID)

#     PortNo=8010
#     if "port" in configPOLL["POLL"]: 
#         PortNo=int(configPOLL['POLL']['port'])
#     SendMSG('Listening on Port : ' + str(PortNo) )

#     POLLgap=30
#     if "Time" in configPOLL["POLL"]:
#         POLLgap=int(configPOLL['POLL']['Time'])

#     SendMSG('Poll Intervals : '+str(POLLgap)+' Seconds')
#     for pin in configPINS:
#         if pin != 'DEFAULT':
#             if configPINS[pin]["Type"]=='AM2302' or  configPINS[pin]["Type"]=='DHT22':
#                 SendMSG('TYPE:HUM/TEMP'+'-'+str(pin)+' '+configPINS[pin]['NAME'])
#             if configPINS[pin]["Type"]=='Relay':
#                 SendMSG('TYPE:RELAY'+'-'+str(pin)+' '+configPINS[pin]['NAME'])

# # ---------------------------------------------------------------------------



        
#     #if 'RLY' in qsp:
#     #    if 'RLY' in qsp:
#     #        return apiRELAY(qsp['RLY'])
#     #    else:
#     #        return 'Type Undefined'
#     else:
#         return 'No Task'

# def apiRELAY(RID):
#     if RID in configPINS:
#         RelayTOGGLE(RID)
#         print('Toggle : ',RID,'-',RelayGET(RID))
#     else:
#         print('Relay not found')

#     return 'OK'
   
# ---------------------------------------------------------------------------

# main function
# Arg1 = R1(relays) or W1(Wire-1) 
# Arg2 = Get/Put
# Arg3 = Relay number 0-7 or SID or nothing
# def main():
#     global GaugeW1
#     SendMSG('Version '+Vers)
#     KillSwitch = ValidatePARMS()
#     if KillSwitch:
#         ReportPARMS()
#         GPIO.setwarnings(False) 
#         GPIO.setmode(GPIO.BCM)
#         start_http_server(PortNo)

#   # Server settings
#   # Choose port 8080, for port 80, which is normally used for a http server, you need root access
#     server_address = ('', 18100)
#     httpd = HTTPServer(server_address, gpioHTTPServer_RequestHandler)
#     httpd.socket.settimeout(1)
#     httpd.handle_request()
#     SendMSG('GPIO API running on 18100')

#     while KillSwitch:    
#         # Wire-1 Sensor Controls
#         SIDs=LISTwire1()

#         # Remove Dead Sensors
#         for ActSid in GaugeW1:
#             if ActSid != 'DEF' and ActSid not in SIDs:
#                 DelPromethues('W1',ActSid)
#                 SendMSG('Sensor Lost : '+ActSid)

#         # Add New Sensors
#         for sid in SIDs:
#             if not isSetPromethues('W1',sid):
#                 AddPromethues('W1',sid)
#                 SendMSG('New Sensor : '+sid)

#         # Read Sensors
#         for sid in SIDs:
#             val = GETwire1('28-'+sid[3:])
#             if val != -999:
#                 UpdPromethues('W1',sid,val)
#             else:
#                 DelPromethues('W1',sid)
#                 SendMSG('Sensor Error : '+sid)    

#         # Read Pins
#         for Pin in configPINS:
#             if Pin != "DEFAULT":
#                 if configPINS[Pin]["Type"]=='AM2302' or configPINS[Pin]["Type"]=='DHT22':
#                     humidity,temperature = Adafruit_DHT.read_retry(22, Pin)
#                     if isinstance(temperature, float):
#                         UpdPromethues('PIN','DHT22_'+Pin+'_TEMP',temperature)
#                     if isinstance(humidity, float):
#                         UpdPromethues('PIN','DHT22_'+Pin+'_HUM',humidity)

#                 if configPINS[Pin]["Type"]=='Relay':
#                     UpdPromethues('PIN','RELAY_'+Pin,RelayGET(Pin) )

#         GapCnt=0
#         while GapCnt <= POLLgap:
#             time.sleep(1)
#             httpd.handle_request()
#             GapCnt+=1


#     sys.stdout.flush()  

 