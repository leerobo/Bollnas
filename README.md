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
` 
sudo python3 -m venv venv
source  venv/bin/activate
`

Load up the enviroment
`
python3 -m pip install -r requirements.txt
`
### Installing on a device

you can install Controller on a RPI or any linux server as a servicectl or docker image
the sensorhub is designed to be installed on a RPI only, due to the GPIO requirements

You can install both controller and sensorhub on the same RPI,  recommend a RPI5 or above 
in docker containers.

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

