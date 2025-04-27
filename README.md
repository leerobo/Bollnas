# The Bollnas Project

Using Grafana and Prometheus to monitor RPIs dotted around the house was always a pain that you had to config prometheus with the APIs and Ports every time,  be it when the DNS reset the IP and i forgot to give it a static IP or the router dies and i have to remember the IPs (happped once,  waste of a weekend that was)

So now promethus just has access to the controller,  which is a set of APIs to force it to scan the LAN for sensorhubs (rpi),  registered them and poll them for metrics.  I will add a little GUI to show the sensorhubs status,  the latest Poll figures of sensors .


## Process
The metric or poll request comes into the Controller, it Polls all the sensorHubs at once if there is NO redis cache (which is about 2 minutes, see config) , it then repackages the reponses or cache data to responsed for the Controller.

But sometimes the responses are slow (old RPIzero) or the zigbee hat needs to reset. so for houses will alot on RPIs or sensors attached i recommend an "autoPoll" Script that calls the Controller /hubs,  This refreshs the cache in the controller.  
Only ever needed to ever run this where i'v had a couple of zigbee hats running on RPIs.  But if you see grafana has gaps , try setting this up

### Requirements
| Packages | Description | |
| ----------- | ----------- | -------------- |
| FastAPI | Python API Framework | |
| pydantic | Data Structure Framework | |
| RPI.GPIO | Hub GPIO Framework | Sensor Hub Only |
| mock.GPIO | Hub GPIO Framework | if not running a RPI |
| redis | Caching framework | Controller only, install docker |


## Setup Enviroment 

Make Directory Github/Bollnas.

#### Install GIT
change main to the branch your working on
``` bash
sudo apt install git
git config --global user.name "ls"
git config --global user.email myEmail@example.com
git config --list

git clone https://github.com/leerobo/Bollnas.git
git pull origin main
```

### Redis   (Controller Only)
docker run -d \
  --name redis \
  -p 6379:6379 \
  -v ~/redis_data:/data \
  --restart always \
  redis:latest 
  

#### Venv
Create a Venv area on the RPI and download required packages
``` bash
sudo python3 -m venv venv
sudo chown pi:pi venv -R
source  venv/bin/activate
python3 -m pip install -r requirements.txt
```

#### Setup Controller
If this is a controller install then nano controller.env in controller directory

``` yml
# Controller Level Secret Details override the Config
netgear_password="BlobblyBob"
```

#### Setup SensorHub
If this is a SensorHub install then nano sensorhub.env in sensorhub directory

``` yml
# Copy straght onto the Device and not part of the gituhb repos pull
api_title = 'The Bollnas Project'
api_description = "Sensor Hub for Main Boiler"

# Security levels between Controllers and SensorHubs
security = True
securityKey = "apiKey"
key = "697984d6-3844-4654-9b89-bcfdb11f5630"

# Wire1 Directory 
wire1 = True

# relays BCD  
relay = True
GPIOrelays  = []
GPIOdescription = {<"26":"Test_Relay"}

# zigbee
zigbee = True
```

### Run 

#### direct

``` bash
cd Bollnas
./run.sh controller        # As a controller   
./run.sh sensorhub         # As a SensorHub
./run.sh                   # As both a controller and sensorhub
```

#### systemd sensorhub
Run These to create the service 
``` bash
sudo cp /home/pi/Bollnas/Scripts/sensorhub.service /lib/systemd/system/
sudo cp /home/pi/Bollnas/Scripts/sensorhub.service /etc/systemd/system/
sudo chmod 644 /lib/systemd/system/sensorhub.service

sudo systemctl daemon-reload
sudo systemctl enable sensorhub
sudo systemctl start sensorhub
sudo systemctl status sensorhub
``` 

Any problem Use this to view the output from the service
``` bash
journalctl -u sensorhub.service -e

```

#### systemd controller
Run These to create the service 
``` bash
sudo cp /home/pi/Bollnas/Scripts/controller.service /lib/systemd/system/
sudo cp /home/pi/Bollnas/Scripts/controller.service /etc/systemd/system/
sudo chmod 644 /lib/systemd/system/controller.service

sudo systemctl daemon-reload
sudo systemctl enable controller
sudo systemctl start controller
sudo systemctl status controller
``` 

Any problem Use this to view the output from the service
``` bash
journalctl -u controller.service -e

```

#### Docker
Trouble here is that RPI.gpio need permission to device,  was thinking to use
PIGPIO or play around with the docker compose abit more ... TODO list

to test go to your web browser and enter your http://<RPi ip>:14121/docs


#### Test
To find your IP address, for local use 127.0.0.1 or accessing a difference device use

``` bash
ip a
# Look at eth0/wlan0 for the inet number 
```

if your on the same device then use <ip>:14120/Docs 


#### Timers & Events AutoPoll 
If you wish to automate the results then use the auto.sh as a template to run in the background
polling the controller .  

### Reference
- GitHub : leerobo/bollnas
- Docker Hub :
