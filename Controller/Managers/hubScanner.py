"""Define the network scanner manager."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from fastapi import BackgroundTasks  # noqa: TC002
from fastapi.responses import JSONResponse
#from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from rich import print as rprint

from Common.Schemas.scannerHubs import Hubs,Hub
from pynetgear import Netgear
import socket,requests
from Controller.Config import getConfig

def scan_lan() -> Hubs:
    Attached_list={}
    if getConfig().netgear_password != "":
      rprint("[orange3]CNTL:     [/orange3][yellow]Logon Netgear Router[/yellow]",getConfig().dns )
      netgear = Netgear(password=getConfig().netgear_password)
      rprint("[orange3]CNTL:     [/orange3][yellow]Scanning Netgear Router[/yellow]" )      
      
      if netgear.login_try_port() :        
        for i in netgear.get_attached_devices():                        # namedTuple Device List
           if i.name != None:
             if i.name not in Attached_list  :  Attached_list[i.name]=i
             if i.type == 'wired' and Attached_list[i.name].type == 'wireless' :  Attached_list[i.name]=i

      else: rprint("[red]CNTL:     [/red]NetGear Error")

    else:
      rprint("[orange3]CNTL:     [/orange3][yellow]LAN scanner[/yellow]",getConfig().dns )
      for i in range(2,250):
        rprint("[orange3]CNTL:     [/orange3][yellow]LAN",i )
        try :
          x = requests.get('http://192.168.1.{}:{}'.format(i,getConfig().sensorHub_port),timeout=1)
          Attached_list[i]={'ip':x}
        except :
          pass  

    # find the SenorHubs
    SensorHubsFound=[]
    for i in Attached_list:
      #rprint('Scanner List',Attached_list[i])
      try:
        x = requests.get('http://{}:{}/info'.format(Attached_list[i].ip,getConfig().sensorHub_port ),timeout=1)      
        SensorHubsFound.append(Hub.from_list(Attached_list[i]))
        rprint("[orange3]CNTL:     [/orange3][yellow]Hub Attached",Attached_list[i].ip,' on Port ',getConfig().sensorHub_port )
      except Exception as e:
        # rprint("[yellow]  -  Not Connect")
        pass

      
    return  Hubs(count=len(SensorHubsFound),SensorHubs=SensorHubsFound)