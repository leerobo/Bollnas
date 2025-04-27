"""Define the network scanner manager."""
from __future__ import annotations
from rich import print as rprint
from Common.Schemas.scannerHubs import Hubs,Hub
from pynetgear import Netgear
from Common.Config import getConfig

import requests
from collections import namedtuple

def scan_lan() -> Hubs:
    Attached_list=[]
    rprint("[orange3]CNTL:     [/orange3][yellow]Scanning ..... [/yellow]" ) 
    # Fixed static LAN addresses
    rprint("[orange3]CNTL:  static {}".format(len(getConfig().static_sensorhubs)) )
    if len(getConfig().static_sensorhubs) > 0 :
      rprint("[orange3]CNTL:     [/orange3][yellow]Static IP List ..... [/yellow]" ) 
      devices=namedtuple('Device',['ip'])
      for i in getConfig().static_sensorhubs:
        try :
          x = requests.get('http://{}:{}/ping'.format(i,getConfig().sensorHub_port),timeout=1)
          Attached_list.append(devices(i))
          rprint("[yellow]INFO:     [/yellow][yellow]Static Address Attached {}[/yellow]".format(i) )      
        except Exception as ex :
          rprint("[yellow]WARNING:     [/yellow][yellow]Static Address Lost {}[/yellow]  ({})".format(i,ex) )      
          pass  

    # Get attached device list directly from the piHole Router
    elif getConfig().pihole_password != "":
      Attached_list={}
      rprint("[orange3]CNTL:     [/orange3][yellow]Scanning Pi-Hole Router[/yellow]" )      
      rprint("[red]ERROR:     [/red]Not Yet Supported" )      

    # Get attached device list directly from the Netgear Router
    elif getConfig().netgear_password != "":
      Attached_list=[]
      netgear = Netgear(password=getConfig().netgear_password)
      rprint("[orange3]CNTL:     [/orange3][yellow]Scanning Netgear Router[/yellow]" )      
      if netgear.login_try_port() :    
        for i in netgear.get_attached_devices_2():                        # namedTuple Device List
           if i.name != None:
             if i.type == 'wired' and Attached_list.type == 'wireless' :  Attached_list=i
      else: rprint("[red]CNTL:     [/red]NetGear Error")

    else:
      # Get attached device list by one by one scanning the LAN (Dead slow)
      rprint("[orange3]CNTL:     [/orange3][yellow]LAN scanner[/yellow]", getConfig().dns )
      for i in range(2,250):
        try :
          x = requests.get('http://192.168.2.{}:{}/ping'.format(i,getConfig().sensorHub_port),timeout=1)
          Attached_list[i]={'ip':x}
        except :
          pass  

    # find the SenorHubs (list must hold dict field ip)
    SensorHubsFound=[]
    for i in Attached_list:
      try:
        x = requests.get('http://{}:{}/ping'.format(i.ip,getConfig().sensorHub_port ),timeout=1) 
        if x.status_code == 200 : 
          hubDetails=Hub(**i._asdict())
          hubDetails.secure=x.json()['security']
          hubDetails.type = x.json()['devicetype']
          hubDetails.name = x.json()['name']
          SensorHubsFound.append( hubDetails )
          rprint("[orange3]CNTL:    [/orange3]",i.ip,"[yellow] Hub Attachedon Port [/yellow] ",getConfig().sensorHub_port )
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