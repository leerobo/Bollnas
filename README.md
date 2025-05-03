# The Bollnas Project

Using Grafana and Prometheus to monitor RPIs dotted around the house was always a pain, Having to config prometheus with the APIs and Ports of every RPI, Then you get a DNS reset and i forgot to give a RPI a static IP or the router dies and i have to remap the IPs (happped once,  waste of a weekend that was)

## Process
So Project Bollnas is one controller that is registered to Promethueus for metrics.  the Controller polls the local network to find other RPI setup as a SensorHub,  these hold Zigbee Hats, Wire 1 Temp sensors and Relays.  
The controller Polls the LAN daily and then every time a /hubs request comes in it polls all the SensorHubs and then compiles the metrics 

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

### Config 
there is a Config.json templete that is loaded into ConfigLoad.py 
This holds the settings for Controllers, SensorHubs, Metrics, openApi Docs and general flags.  

Word too the wise
The github Config_Template.json needs to be renamed to Config.json for your settings,  dont upload it to github with passwords and IPs in there.  

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
As the system only updates metrics when the Controller /hubs is called, you need to 
Poll this every xx seconds,  
There are 2 options 
Easyest option is crontab to execute curl localhost:14121/hubs every minute or 2
or 
Create a background script to run and put it in sleep mode for xx seconds before calling a request to /hubs

I dont need second by second readings,  so i use cron to poll every 2 minutes
*/2 * * * * curl -X GET localhost:14121/hubs




### Reference
- GitHub : leerobo/bollnas
- Docker Hub :
