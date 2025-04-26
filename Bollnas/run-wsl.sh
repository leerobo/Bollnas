#!/bin/bash
if [ "$1" == "controller" ]; then
 echo "Controller Device"
 export CONTROLLER=True
 export SENSORHUB=False
elif [ "$1" == "sensorhub" ]; then
 echo "SensorHub Device"
 export CONTROLLER=False
 export SENSORHUB=True
else
 echo "Controller & SensorHub Device"
 export CONTROLLER=True
 export SENSORHUB=True
fi

echo "Github Update"
git pull origin sensorhub
echo "Github API start "
cd /home/lero/Github/Bollnas

/home/lero/Github/Home/Bollnas/venv/bin/python3 /home/lero/Github/Home/Bollnas/venv/bin/fastapi dev /home/lero/Github/Home/Bollnas/Bollnas/runapp.py --port 14121 --host 0.0.0.0
