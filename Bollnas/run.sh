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

# Keeps software up to date , but if it falls out of line just run the git pull command manually
# remove any files that are clashiinng (due to merge) and run again 
if [ "$1" != "noupdate" ] && [ "$2" != "noupdate" ]; then
    echo "Github Update"
    git pull origin main
    echo "Github API starting"
fi    

export ROOTPATH="/home/$USER/Bollnas"

# $ROOTPATH/venv/bin/python3 $ROOTPATH/venv/bin/fastapi dev $ROOTPATH/Bollnas/runapp.py --port 14121 --host 0.0.0.0
python3 $ROOTPATH/venv/bin/fastapi dev $ROOTPATH/Bollnas/runapp.py --port 14121 --host 0.0.0.0
