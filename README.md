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

Sudo apt Update
Sudo apt Upgrade

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

You might need to install pip first
sudo apt install pip 

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

To install : https://raspberrytips.com/docker-on-raspberry-pi/

When scanning the LAN, there are 3 ways to do it.  
1. Get the list of attached devices from your router
2. Hold a static list of IPs for your Devices
3. Go thru a IP range 

option 3, is the slowest and not overly clever,  option 2 is the quickest but will not find new devices.  option 1 is the middle ground. 
To get option 1 enter your router password,  currently support netgear , but am working on pihole for later aswell.

options 2 set Statis_Sensorhubs list with the ip addresses.

if nothing set ,  option 3 will happen


#### Setup SensorHub
if Wire1 is true ,  make sure you have set this on via raspi-config.  then attached the sensors to pin 1 Power,7 Data,9 Gnd

if Zigbee, (lee do this when you know whats involved)

Relays holds a list of pins & Descriptions,  when the system starts up the pins here are sent to outgoing and pulled down .. Off.  

### Run 
#### direct

``` bash
cd Bollnas
./run.sh controller        # As a controller   
./run.sh sensorhub         # As a SensorHub
./run.sh                   # As both a controller and sensorhub
```

When run executes it updates the code with the latest from github,  to stop this add noupdate to the run command.
``` bash
./run.sh controller noupdate # As a controller   

```
Usefull if your playing around with the code


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

#### Test
To find your IP address, for local use 127.0.0.1 or accessing a difference device use

``` bash
ip a
# Look at eth0/wlan0 for the inet number 
```

to test go to your web browser and enter your http://<RPi ip>:14121/docs
you should see the swagger API screen 

#### Timers & Events AutoPoll 
As the system only updates metrics when the Controller /hubs is called, you need to 
Poll this every xx seconds,  
There are 2 options 
Easyest option is crontab to execute curl localhost:14121/hubs every minute or 2
or 
Create a background script to run and put it in sleep mode for xx seconds before calling a request to /hubs

I dont need second by second readings,  so i use cron to poll every 2 minutes
*/2 * * * * curl -X GET localhost:14121/hubs

just remember the Cache config holds the sensor data for xx seconds set by the Timer,  make sure this is greater than your cron/script poll


### Prometheus 
``` bash
  - job_name: 'BollnasController'
    follow_redirects: true
    metrics_path: /metrics/
    static_configs:
    - targets: ['bollnascontroller.local:14121']
```
### Zigbee 
#### DeconZ
https://github.com/deconz-community/deconz-docker/tree/main

### Reference
- GitHub : leerobo/bollnas
- Docker Hub :
