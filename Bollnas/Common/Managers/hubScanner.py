"""Define the network scanner manager."""
from __future__ import annotations
from rich import print as rprint
from Common.Schemas.scannerHubs import Hubs,Hub
from pynetgear import Netgear
from Common.Config import getConfig

import requests

def scan_lan() -> Hubs:
    Attached_list={}

    # Get attached device list directly from the Router
    if getConfig().netgear_password != "":
      rprint("[orange3]CNTL:     [/orange3][yellow]Logon Netgear Router[/yellow]",getConfig().dns )
      netgear = Netgear(password=getConfig().netgear_password)
      rprint("[orange3]CNTL:     [/orange3][yellow]Scanning Netgear Router[/yellow]" )      

      if netgear.login_try_port() :    
        for i in netgear.get_attached_devices_2():                        # namedTuple Device List
           if i.name != None:
             if i.name not in Attached_list  :  Attached_list[i.name]=i
             if i.type == 'wired' and Attached_list[i.name].type == 'wireless' :  Attached_list[i.name]=i
      else: rprint("[red]CNTL:     [/red]NetGear Error")

    else:
      # Get attached device list by one by one scanning the LAN (Dead slow)
      rprint("[orange3]CNTL:     [/orange3][yellow]LAN scanner[/yellow]",getConfig().dns )
      for i in range(2,250):
        try :
          x = requests.get('http://192.168.2.{}:{}/ping'.format(i,getConfig().sensorHub_port),timeout=1)
          Attached_list[i]={'ip':x}
        except :
          pass  

    # find the SenorHubs
    SensorHubsFound=[]
    for i in Attached_list:
      #  rprint('\nScanner List',Attached_list[i])
      try:
        x = requests.get('http://{}:{}/ping'.format(Attached_list[i].ip,getConfig().sensorHub_port ),timeout=1) 
        if x.status_code == 200 : 
          hubDetails=Hub(**Attached_list[i]._asdict())
          hubDetails.secure=x.json()['security']
          SensorHubsFound.append( hubDetails )
          rprint("[orange3]CNTL:     [/orange3]",Attached_list[i].ip,"[yellow] Hub Attachedon Port [/yellow] ",getConfig().sensorHub_port )
        else:   
          rprint("[orange3]CNTL:     [/orange3]",Attached_list[i].ip,"[yellow] Port Found, Bad Response[/yellow] (",x.status_code,")")

      except requests.exceptions.ConnectionError as e:
        # rprint("[yellow]Warning   :[/yellow]Connection Error - ",Attached_list[i].ip,' >>>> ',e)
        pass
      except requests.exceptions.HTTPError as e:
        # rprint("[yellow]Warning   :[/yellow]HTTP Error - ",Attached_list[i].ip,' >>>> ',e)
        pass
      except requests.exceptions.RequestException as e:
        # rprint("[yellow]Warning   :[/yellow]Request Error - ",Attached_list[i].ip,' >>>> ',e)
        pass

      except Exception as e:
        rprint("[red]Error   :[/red]Response Error - ",Attached_list[i].ip,' >>>> ',e)
        pass
      
    return  Hubs(count=len(SensorHubsFound),SensorHubs=SensorHubsFound)