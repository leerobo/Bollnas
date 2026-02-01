"""Define routes for Authentication."""
from rich import print as rprint                          ## Pretty Print
import traceback

#from Bollnas.Common.zzzzzConfig import getConfig
from Common.ConfigLoad import getJSONconfig

import Common.Models.enums as enums

import prometheus_client as prom 
from prometheus_client import Enum, Counter, Gauge, Histogram 
from prometheus_client.metrics import _build_full_name   

# TODO :  Workout if you lost a sensor
def setPrometheusMetrics(Schema:list):
      rprint("[orange3]CNTL:     [/orange3][yellow]Building Prometheus Metrics[/yellow]")
      HubName=Schema.hubName 
      SubHubName=Schema.subHubName

      rprint("[orange3]CNTL:     [/orange3][yellow]Hub Metrics[/yellow]",Schema)

      for pins in Schema.GPIOsettings:
         if pins.status == enums.GPIOstatus.ok:
            try:
               fullName=_build_full_name(metric_type='enum',name='P'+str(pins.pin),
                                   namespace=HubName,subsystem=SubHubName,
                                   unit='')
 
               if fullName in prom.REGISTRY._names_to_collectors:
                  rprint("[orange3]CNTL:     [/orange3][yellow]Update Metrics[/yellow]",fullName)
                  e =  prom.REGISTRY._names_to_collectors[fullName]
               else: 
                  rprint("[orange3]CNTL:     [/orange3][yellow]New Metrics[/yellow]",fullName)
                  e = Enum(
                     namespace=getJSONconfig().Installation.Location ,
                     subsystem=getJSONconfig().Installation.Room+'_'+getJSONconfig().Installation.Room ,
                     name='P'+str(pins.pin),
                     documentation='BCD Pin-{}'.format(pins.pin),
                     states=['on', 'off', 'unknown']
                  )
               if   pins.value == 0 :  e.state('on')            
               elif pins.value == -1 : e.state('unknown') 
               else :                  e.state('off')
            except Exception as ex:
               rprint("[red]CNTL:     [/red]",fullName,':',ex)
               traceback.print_exc()
               return

      for W1 in Schema.wire1Sensors:
            fullName=_build_full_name(metric_type='enum',name=W1.id[3:],
                                   namespace=HubName,subsystem=SubHubName,
                                   unit='')            
            try:
               if fullName in prom.REGISTRY._names_to_collectors:
                  rprint("[orange3]CNTL:     [/orange3][yellow]Update Metrics[/yellow]",fullName)
                  e =  prom.REGISTRY._names_to_collectors[fullName]
               else: 
                  rprint("[orange3]CNTL:     [/orange3][yellow]New Metrics[/yellow]",fullName)
                  e = Gauge(
                     namespace=HubName,subsystem=SubHubName,
                     name=W1.name,
                     documentation=str(W1.type.name)+'-'+str(W1.measurement.value)
                  )
               e.set(W1.value)            
            except Exception as ex:
               rprint("[red]CNTL:     [/red]",fullName,':',ex)