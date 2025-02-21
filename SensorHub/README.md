# The Bollnas Project

## SensorHub Config and Setup 
Sensorhub uses RPI.GPIO within a venv python enviroment, so running with a docker enviroment is tricky to setup 
so it has access to the GPIO of the device,  so i run it as a Daemon service which allows easy access to the GPIO

If you want to go for a docker enviroment,  then maybe try PIGPIO 

in ConfigSensorHb.settings
``` yml
# Wire1 Directory        <<<<<<<<<< Allows you to allocate a name to an ID if you want to
wire1Dir: str = "/sys/bus/w1/devices/"
WIRE1description: dict = {}

# relays BCD             <<<<<<<<<< Allows you to allocate a GPIO to a name if you want to
GPIOrelays: list[int] = []
GPIOdescription: dict = {}
```

If no Relays attached to GPIO then set to :-
``` yml
   GPIOrelays: list[int] = [] 
   GPIOdescription: dict = {}
```   

### Systemmd Service setup

sudo raspi-config
- Set WiFi password and ssid
- Set RPI to Wire1 or Serial (Zigbee) (if required) 
- Set SSH to open 
- make a note of ip
```    bash
ip a
``` 

Note : If you wanted to you could update code directly from github but you would need to setup the RPI to do that

- sudo reboot

From this point you can use putty 
- sudo apt update
- sudo apt upgrade
- mkdir /Github/Bollnas
- Copy Code to RPI (i use filezilla)
- Build the venv for you device might need to install   > sudo apt-get install python3-venv
``` bash
cd home/pi/Github/Bollnas
sudo python3 -m venv venv  (Takes a min)
source  venv/bin/activate
python3 -m pip install -r requirements.txt
```

if you need to upgrade python then do it either at device level or in venv level , look at https://www.python.org/downloads/ for the latest version and change the following .tgz to match
``` bash
wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz
cd Python-3.12.4
./configure --enable-optimizations
sudo make altinstall
```
atlinstall take hours on a Zero/30 mins RPI3/15 mins RPI5

change python3 to the newer verison 
``` bash
cd /venv/bin
sudo rm python3
sudo ln -s /usr/local/bin/python3.12 python3
python3 --version
```

this will compile python up

to test install 
- cd SensorHub
- ./sensorhub.sh
if it works move on , if not FIX it

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
You can setup the controller either as a docker container or as a system.service (like the sensorhub) 

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

#### Timers & Events AutoPoll 
If you wish to automate the results then use the auto.sh as a template to run in the background
polling the controller .  


### Reference
- GitHub : leerobo/bollnas
- Docker Hub :


### RPIzero setup (github pull)

- Clean Image python 3.11
- sudo apt update
- sudo apt upgrade 

- sudo apt install git
- sudo apt install -y gh

- gh auth login

- git config --global user.name "myGitHubUser"
- git config --global user.email myEmail@example.com
- git config --list

- git remote add origin 'your_url_name'




