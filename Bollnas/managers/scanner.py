"""Define the network scanner manager."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from fastapi import BackgroundTasks  # noqa: TC002
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from rich import print as rprint

from Bollnas.config.settings import get_settings
from pynetgear import Netgear
import socket,requests

def scan_lan():
    Attached_list={}
    print('pws',get_settings().netgear_password )
    if get_settings().netgear_password != "":
      rprint("[yellow]TASK:     [/yellow][bold]Logon Netgear Router",get_settings().dns )
      netgear = Netgear(password=get_settings().netgear_password)
      rprint("[yellow]TASK:     [/yellow][bold]Scanning Netgear Router",get_settings().dns )
      

      if netgear.login_try_port() :
        for i in netgear.get_attached_devices():
           if i.name != None:
             if i.name not in Attached_list :  Attached_list[i.name]=i
             if i.type == 'wired' and Attached_list[i.name].type == 'wireless' :  Attached_list[i.name]=i
      else: rprint("[red]ERROR:   [/red][bold]NetGear Logon Error",get_settings().dns )  

    else:
      rprint("[yellow]TASK:     [/yellow][bold]Scanning",get_settings().dns)
      for i in range(2,250):
        try :
          x = requests.get('http://192.168.1.{}'.format(i),timeout=1)
          Attached_list[i]={'ip':x}
        except :
          pass  

    # find the SenorHubs
    hubs={}
    for i in Attached_list:
      rprint('Scanner List',Attached_list[i])
      rprint("[purple]DEBUG:    [/purple][bold]Scanning",Attached_list[i].ip,'-',get_settings().sensorHub_port)
      try:
        x = requests.get('http://{}:{}/info'.format(Attached_list[i].ip,get_settings().sensorHub_port ),timeout=1)
        rprint("[yellow]HUB:      [/yellow][bold]Sensor Hub Found @", Attached_list[i].ip) 
        hubs[i]=Attached_list[i]
      except Exception as e:
        print(e)  
      
    return  hubs