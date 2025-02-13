#!/usr/bin python3
    
import sys, os, time, datetime, glob, json
from array import array
from typing import Union

import Common.Schemas.Sensors.gpio as gpio
import Common.Schemas.Sensors.wire1 as wire1
import Common.Models.enums as enums

from rich import print as rprint
from SensorHub.Config import getConfig, setConfig, Settings
from SensorHub.Config import ConfigDict
import requests

try:
    # checks if you have access to RPi.GPIO, which is available inside RPi
    import RPi.GPIO as GPIO
except Exception as ex:
    # In case of exception, you are executing your script outside of RPi, so import Mock.GPIO
    #import Mock.GPIO as GPIO
    rprint('[yellow]WARNING       [/yellow]Loaded Mock RPI ',ex)



async def poll(): 
    rtn={}
    rtn['timestamp']=str(datetime.datetime.now())
    if getConfig().wire1 : rtn['wire1Sensors']=pollWire1()
    if getConfig().relay :rtn['GPIOsettings']=pollGPIO()
    if getConfig().zigbee :rtn['zigbee']=pollZigbee()
    rprint('Poll :',rtn)    
    return rtn
          
# ---------------- WIRE 1 find and read --------------------

def pollWire1() -> list[wire1.Status]:
    """ ## Wire 1 Poll
    On RPI on sensors Wire-1 connects are held in the wireDir1 directory,
    This scans the Directory for the files,  one file, one sensor.
    """
    wire1Sensors=[]
    SIDs=[]
    devicelist = glob.glob(getConfig().wire1dir+'28*')   #  DS18 Sensors

    if devicelist!='':
        for device in devicelist:
            TT=device.split("/")
            SID = TT[len(TT)-1]
            sensorVal=readWire1(SID)
            print(sensorVal)
            if sensorVal > -999:
               print(SID)
               wire1Sensors.append( wire1.Status(
                                 id='W1_S'+SID[3:], 
                                 type=enums.SensorType.DS18B20, 
                                 measurement=enums.SensorMeasurement.c, 
                                 platform=enums.SensorPlatform.wire1, 
                                 value=sensorVal,
                                 description=getDescriptions('W1_S'+SID[3:])
                                 )  )

    return wire1Sensors
def readWire1(SID) -> float:
    """ Read Wire 1 sensors from Directory based on Sensor ID(File name) """
    devicefile=getConfig().wire1dir+SID+'/w1_slave'
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
def pollGPIO()  -> list[gpio.Pins]:
    rprint('[yellow]GPIO Scanning')
    rtn=[]
    try:
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        for relay in getConfig().GPIOrelays:
            # GPIO.setup(int(relay), GPIO.OUT)
            rtn.append( GPIOread( gpio.Pins(pin=relay,pintype=enums.GPIOdeviceAttached.relay,
                                            direction=enums.GPIOdirection.out,
                                            status=enums.GPIOstatus.ok,
                                            description=getDescriptions(relay))  ) )
    except Exception as ex:
        rprint('[red]Sensor Read Error : {}'.format(ex) )
        rtn.append( GPIOread( gpio.Pins(pin=relay,pintype=enums.GPIOdeviceAttached.relay,
                                        direction=enums.GPIOdirection.out,
                                        status=enums.GPIOstatus.error,value=-86,
                                        description=getDescriptions(relay)
                                       )  )  )
    return rtn
def getDescriptions(pinW1) -> str:
    print('Get description >>>',pinW1,getConfig().GPIOdescription)
    if str(pinW1) in getConfig().GPIOdescription:  return getConfig().GPIOdescription[str(pinW1)]
    if str(pinW1) in getConfig().wire1description: return getConfig().wire1description[str(pinW1)]
    return ""

# ---------------- GPIO Pin Reads --------------------

# Return Pin ON/OFF status
#def pollZigbee()  -> list[gpio.Zigbee]:
def pollZigbee() :
    rprint('[yellow]Zigbee Scanning ',getConfig().ZBuser)
    if getConfig().ZBuser == '': 
       user,status=ZBconnect,status = getZBuser() 
       if status != 200 : return ZBconnect
       rprint('[orange3]ZIGBEE     [/orange3]Set Config ZBuser too ',user['username'])
       return {'message':'Set Config ZBuser too '+user['username']}
    # else:
    #    user,status=ZBconnect,status = getZBkey() 
    #    if status != 200 : return ZBconnect
    #    rprint('[orange3]ZIGBEE     [/orange3]Set Config ZBkey too ',user['username'])
    #    return {'message':'Set Config ZBkey too '+user['username']}

    ZBconnect,status = getZBconfig() 
    if status != 200 : return ZBconnect
    rprint('[orange3]ZIGBEE     [/orange3]Set Config ZBkey too ',ZBconnect)

    ZBconnect,status = getZBsoftwareUpd() 
    if status != 200 : return ZBconnect
    rprint('[orange3]ZIGBEE     [/orange3]Set Software ZBkey too ',ZBconnect)

    ZBconnect,status = getZBfirmwareUpd() 
    if status != 200 : return ZBconnect
    rprint('[orange3]ZIGBEE     [/orange3]Set Fireware ZBkey too ',ZBconnect)





    return {'message':'Set Config ZBkey too ','data':ZBconnect}
 
def findZBhub() -> tuple[dict,int]:
    rprint('[yellow]Zigbee Find')
    try:
      rprint('ZBport',getConfig().ZBport)
      resp=requests.post('http://127.0.0.1:{}/api'.format(getConfig().ZBport),data='{"devicetype":"Bollnas"}',timeout=2)
      rprint('[yellow]ZIGBEE:     [/yellow]',resp.status_code,':',resp.json())
      if resp.status_code != 200 : return resp.json(),resp.status_code
      rprint('[yellow]ZIGBEE:     [/yellow]',resp.json())
      return resp.json(),200
    except Exception as ex:  
      rprint('[red]ZIGBEE:      Error:[/red]-',ex)
      return {'message':ex},403

def getZBuser() -> tuple[dict,int]:
    rprint('[yellow]Zigbee    :[/yellow]Get User on',getConfig().ZBdevice)
    body={"devicetype": getConfig().ZBdevice }
    try:
      resp=requests.post('http://127.0.0.1:{}/api'.format(getConfig().ZBport),data=json.dumps(body),timeout=2)
      if resp.status_code != 200 : return resp.json(),resp.status_code 
      if 'success' not in resp.json()[0] : return {'message': resp.json() },403
      return resp.json()[0]['success'],200
    except Exception as ex:  
      rprint('[red]Zigbee      :[/red]User Get -',ex)
      return {'message':ex},403

def getZBconfig() -> tuple[dict,int]:
    rprint('[yellow]Zigbee    :[/yellow]Get Config on',getConfig().ZBdevice)
    try:
      resp=requests.get('http://127.0.0.1:{}/api/{}/config'.format(getConfig().ZBport,getConfig().ZBuser),timeout=2)
      if resp.status_code != 200 : return resp.json(),resp.status_code 
      return resp.json(),200
    except Exception as ex:  
      rprint('[red]Zigbee      :[/red]Config Get -',ex)
      return {'message':ex},403

def getZBsoftwareUpd() -> tuple[dict,int]:
    rprint('[yellow]Zigbee    :[/yellow]Update Software on',getConfig().ZBdevice)
    try:
      resp=requests.get('http://127.0.0.1:{}/api/{}/config/update'.format(getConfig().ZBport,getConfig().ZBuser),timeout=2)
      if resp.status_code != 200 : return resp.json(),resp.status_code 
      return resp.json(),200
    except Exception as ex:  
      rprint('[red]Zigbee      :[/red]Software Update Get -',ex)
      return {'message':ex},403

def getZBfirmwareUpd() -> tuple[dict,int]:
    rprint('[yellow]Zigbee    :[/yellow]Update firmware on',getConfig().ZBdevice)
    try:
      resp=requests.get('http://127.0.0.1:{}/api/{}/config/updatefirmware'.format(getConfig().ZBport,getConfig().ZBuser),timeout=2)
      if resp.status_code != 200 : return resp.json(),resp.status_code 
      return resp.json(),200
    except Exception as ex:  
      rprint('[red]Zigbee      :[/red]Software Update Get -',ex)
      return {'message':ex},403


# Control GPIO Pins 
def GPIOread(pin: gpio.Pins) -> gpio.Pins:
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
def GPIOset(pinReq:gpio.Pins,task:enums.GPIOtask) -> gpio.Pins:
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
