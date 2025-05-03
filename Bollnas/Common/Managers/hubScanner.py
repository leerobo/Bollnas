"""Define the network scanner manager."""
from __future__ import annotations
from rich import print as rprint
from Common.Schemas.scannerHubs import Hubs,Hub
from pynetgear import Netgear
#from Bollnas.Common.zzzzzConfig import getConfig,getControllerConfig,getSensorHubConfig
from Common.ConfigLoad import getJSONconfig
from Common.helpers import get_project_root

import requests
from collections import namedtuple

def scan_lan() -> Hubs:
    Attached_list=[]
    rprint("[orange3]CNTL:     [/orange3][yellow]Scanning ..... [/yellow]")  
    # Fixed static LAN addresses
 
    if len(getJSONconfig().ControllerHub.Static_Sensorhubs) > 0:
      rprint("[orange3]CNTL:     [/orange3][yellow]Static IP List ..... [/yellow]" ) 
      devices=namedtuple('Device',['ip'])
      for i in getJSONconfig().ControllerHub.Static_Sensorhubs:
        try :
          x = requests.get('http://{}:{}/ping'.format(i,getJSONconfig().ControllerHub.sensorHub_port),timeout=1)
          Attached_list.append(devices(i))
          rprint("[yellow]INFO:     [/yellow][yellow]Static Address Attached {}[/yellow]".format(i) )      
        except Exception as ex :
          rprint("[yellow]WARNING:     [/yellow][yellow]Static Address Lost {}[/yellow]  ({})".format(i,ex) )      
          pass  

    # Get attached device list directly from the piHole Router
    elif getJSONconfig().ControllerHub.piHole_Pwd != "":
      Attached_list=[]
      rprint("[orange3]CNTL:     [/orange3][yellow]Scanning Pi-Hole Router[/yellow]" )      
      rprint("[red]ERROR:     [/red]Not Yet Supported" )      

    # Get attached device list directly from the Netgear Router
    elif getJSONconfig().ControllerHub.Netgear_Pwd != "":
      Attached_list=[]
      netgear = Netgear(password=getJSONconfig().ControllerHub.Netgear_Pwd,host=getJSONconfig().ControllerHub.dns )

      rprint("[orange3]CNTL:     [/orange3][yellow]Scanning Netgear Router[/yellow] ",getJSONconfig().ControllerHub.Netgear_Pwd, " @ ",getJSONconfig().ControllerHub.dns  )      
      if netgear.login_try_port() :    
        for i in netgear.get_attached_devices_2():                        # namedTuple Device List
           #rprint(i)
           if i.name != None:     Attached_list.append(i)
      else: rprint("[red]CNTL:     [/red]NetGear Error")

    else:
      # Get attached device list by one by one scanning the LAN (Dead slow)
      rprint("[orange3]CNTL:     [/orange3][yellow]LAN scanner[/yellow]", getJSONconfig().ControllerHub.dns )
      for i in range(2,250):
        try :
          x = requests.get('http://192.168.2.{}:{}/ping'.format(i,getJSONconfig().ControllerHub.Port_Scanner),timeout=1)
          Attached_list[i]={'ip':x}
        except :
          pass  

    # find the SenorHubs (list must hold dict field ip)
    SensorHubsFound=[]
    for i in Attached_list:
      try:
        x = requests.get('http://{}:{}/ping'.format(i.ip,getJSONconfig().ControllerHub.Port_Scanner ),timeout=1) 
        if x.status_code == 200 : 
          hubDetails=Hub(**i._asdict())
          hubDetails.secure=x.json()['security']
          hubDetails.type = x.json()['devicetype']
          hubDetails.name = x.json()['name']
          SensorHubsFound.append( hubDetails )
          rprint("[orange3]CNTL:    [/orange3]",i.ip,"[yellow] Hub Attached on Port [/yellow] ",getJSONconfig().ControllerHub.Port_Scanner )
        else:   
          rprint("[orange3]CNTL:    [/orange3]",i.ip,"[yellow] Port Found, Bad Response[/yellow] (",x.status_code,")")

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
        rprint("[red]Error   :[/red]Response Error - ",i.ip,' >>>> ',e)
        pass

    return  Hubs(count=len(SensorHubsFound),SensorHubs=SensorHubsFound)