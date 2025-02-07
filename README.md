# The Bollnas Project

Using Grafana and Prometheus to monitor RPIs dotted around the house was always a pain that you had to config prometheus with the APIs and Ports every time i added a RPI or the DNS hit the wall and everything has a different IP address.

So now promethus just has access to the controller,  which is a set of APIs then force it to scan the LAN,  find sensorhubs,  registered them and them continue to poll them.  This allowed me to see realtime the RPIs status via the controllers Status API and uses the promethues Client repos to allow my main server to get the info and store it. 

The sensorshub polls the sensors and relay pins and stores the settings ready for the next controller request,  it can also accept requests to toggle the relay pins via the controller.

| Packages | Description | 
| ----------- | ----------- |
| FastAPI | Python API Framework |
| pydantic | Data Structure Framework |
| RPI.GPIO | Hub GPIO Framework |
| redis | Caching framework |


### Configs
- .envcontroller : Controller Setup Details
- .envsensorhub  : SensorHub Setup Details
- .env : Setup package details used by Framework

### Setup
Create a Venv area on the RPI
``` bash
sudo python3 -m venv venv
source  venv/bin/activate
```

Load up the enviroment
``` bash
python3 -m pip install -r requirements.txt
```
### Installing on a device

you can install Controller on a RPI or any linux server as a servicectl or docker image
the sensorhub is designed to be installed on a RPI only, due to the GPIO requirements

You can install both controller and sensorhub on the same RPI,  recommend a RPI5 or above 
in docker containers.


#### SensorHub Config and Setup 

in ConfigSensorHb.settings
``` yml
# Wire1 Directory        <<<<<<<<<< Allows you to allocate a name to an ID
wire1Dir: str = "/sys/bus/w1/devices/"
WIRE1description: dict = {'W1_S011937e722c2':'Outside'}

# relays BCD             <<<<<<<<<< Allows you to allocate a GPIO to a name
GPIOrelays: list[int] = [12,16,20,21]
GPIOdescription: dict = {'12':'Relay 1','16':'Relay 2'}
```

If no Relays attached to GPIO then set to GPIOrelays: list[int] = [] 

#### Systemmd Service setup

sensorhub runs within the venv area, which means it has access to RPi.gpio (unlike docker - can use pigpio if you want docker), Ammend the Scripts.sensorhub.service if you wish to use a different port number

Run These to create the service 
``` bash
sudo cp /home/pi/Github/Bollnas/Scripts/sensorhub.service /lib/systemd/system/
sudo cp /home/pi/Github/Bollnas/Scripts/sensorhub.service /etc/systemd/system/
sudo chmod 644 /lib/systemd/system/sensorhub.service

sudo systemctl daemon-reload
sudo systemctl enable sensorhub
sudo systemctl start sensorhub
sudo systemctl status sensorhub
``` 

Any problem Use this to view the output from the service
``` bash
journalctl -u sensorhub.service

```

to test go to your web browser and enter your http://<RPi ip>:14121/docs

To find your IP address
``` bash
ip a
# Look at eth0/wlan0 for the inet number 
```



#### Controller
if running via docker,  run dockerbuild to get the latest image
`
docker compose 
`

if running via systemctl then pull the latest github source 

once installed amend the .venvcontroller variables
`
CONTROLLER_NAME="Bollnas"
CONTROLLER_DESCRIPTION="The Bollnas Project"
`

#### Timers & Events
If you wish to automate the results then use the auto.sh as a template to run in the background
polling the controller .  Useful to control relays, lights depending on the polled results.


### Reference
- GitHub : leerobo/bollnas
- Docker Hub :

