#!/usr/bin python3
from rich import print as rprint
try:
    # checks if you have access to RPi.GPIO, which is available inside RPi
    import RPi.GPIO as GPIO
except:
    # In case of exception, you are executing your script outside of RPi, so import Mock.GPIO
    rprint("[yellow]WARNING:  [/yellow]Running Mock GPIO on non RPI Device > pip install rpi.gpio")
    import Mock.GPIO as GPIO
    
import sys, os, time, datetime, glob
# from array import array
# from typing import Union

import Common.Schemas.poll as Pollschema
import Common.Schemas.Sensors.gpio as gpio
import Common.Schemas.Sensors.wire1 as wire1
import Common.Models.enums as enums
from Common.ConfigLoad import getJSONconfig

async def poll(): 
    rtn=Pollschema.Poll(timestamp=str(datetime.datetime.now()),
                   hubName=getJSONconfig().Installation.Room,
                   subHubName=getJSONconfig().Installation.Reason)
    # rtn['timestamp']=str(datetime.datetime.now())
    # rtn['hubName']=getJSONconfig().Installation.room
    # rtn['subHubName']=getJSONconfig().Installation.Reason
    rtn.wire1Sensors=pollWire1()
    rtn.GPIOsettings=pollGPIO()
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
    if not getJSONconfig().SensorHubs.Wire1 : return wire1Sensors

    devicelist = glob.glob(getJSONconfig().SensorHubs.Wire1dir+'28*')   #  DS18 Sensors

    if devicelist!='':
        for device in devicelist:
            TT=device.split("/")
            SID = TT[len(TT)-1]
            sensorVal=readWire1(SID)
            if sensorVal > -999:
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
    devicefile=getJSONconfig().SensorHubs.Wire1dir+SID+'/w1_slave'
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
        for relay in getJSONconfig().SensorHubs.Relays:
            pinDetails=GPIOread( gpio.PinChange(pin=relay['pin'],task=enums.GPIOtask.read) )
            if pinDetails.value == None:
               pinDetails.value = -88
               pinDetails.reason = 'Unknown State Found'  

            rtn.append( gpio.Pins(pin=relay['pin'],pintype=enums.GPIOdeviceAttached.relay,
                                  direction=enums.GPIOdirection.out,
                                  status=pinDetails.status,
                                  value=pinDetails.value,
                                  reason=pinDetails.reason,
                                  description=getDescriptions(relay))  ) 
       
    except Exception as ex:
        rprint('[red]Sensor {} Read Error : {}'.format(relay,ex) )
        rtn.append( GPIOread( gpio.Pins(pin=relay['pin'],pintype=enums.GPIOdeviceAttached.relay.value,
                                        direction=enums.GPIOdirection.out,
                                        status=enums.GPIOstatus.error,value=-86,
                                        description=getDescriptions(relay)
        )  )  )
    return rtn
def getDescriptions(pinW1) -> str:
    for relay in getJSONconfig().SensorHubs.Relays:
        if str(pinW1) in relay['pin'] : return relay['Description']
    return ""

# Control GPIO Pins 
def GPIOread(pinReq:gpio.PinChange) -> gpio.PinChange:
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinReq.pin, GPIO.OUT)
    try:
       pinReq.value = GPIO.input(pinReq.pin)
       pinReq.status = enums.GPIOstatus.ok
       return pinReq
    except Exception as ex:
       rprint('[red]GPIO Read Error ',pinReq.pin,':',ex)
       pinReq.value = -85
       pinReq.status = enums.GPIOstatus.error
       pinReq.reason = str(ex)
       return pinReq
    
def GPIOset(pinReq:gpio.PinChange) -> gpio.Pins:
    GPIO.setmode(GPIO.BCM)
    pin = gpio.Pins(pin=pinReq.pin,pintype=enums.GPIOdeviceAttached.relay,status=enums.GPIOstatus.unknown)
    pinRead=GPIOread(pinReq)
    if pinRead.status != enums.GPIOstatus.ok:      return pin 

    try:
       if   pinReq.task == enums.GPIOtask.toggle and pinRead.value == 0 :
             GPIO.output(pinReq.pin, 1)
             pin.value=1
       elif pinReq.task == enums.GPIOtask.toggle and pinRead.value == 1 :
             GPIO.output(pinReq.pin, 0)
             pin.value=0
       elif pinReq.task == enums.GPIOtask.on :
             GPIO.output(pinReq.pin, 0)
             pin.value=0
       else : 
             GPIO.output(pinReq.pin, 1)
             pin.value=1

       return  pin
    
    except Exception as ex:
        rprint('[red]GPIO Error : {}'.format(ex) )
        pin.status=enums.GPIOstatus.error
        pin.value=-86
        pin.reason = str(ex)
        rprint('[red]GPIO       : {}'.format(pinReq) )
        return pin
    
def GPIOinit(pin:gpio.PinChange) -> bool:
    GPIO.setmode(GPIO.BCM)
    try:
       GPIO.setup(pin.pin, GPIO.OUT, initial= 1)
       #rprint('[yellow]GPIO {} set to Out Relay '.format(pin.pin) )
       return True
    except Exception as ex:
       rprint('[red]GPIO {} Pin Set Error : {}'.format(pin.pin,ex) )
       return False
    
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
