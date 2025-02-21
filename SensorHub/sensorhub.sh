export LOADTYPE="sensorhub" 
git pull origin sensorhub
fastapi dev mainSensorhub.py --port 14121 --host 0.0.0.0 
