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

#export ROOTPATH = "/home/$USER/Bollnas"
export ROOTPATH="/home/$USER/Home/Bollnas"

$ROOTPATH/venv/bin/python3 $ROOTPATH/venv/bin/fastapi dev $ROOTPATH/Bollnas/runapp.py --port 14121 --host 0.0.0.0
