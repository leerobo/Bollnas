export LOADTYPE="sensorhub" 
echo "Github Update"
git pull origin sensorhub
echo "Github API start "
fastapi dev mainSensorhub.py --port 14121 --host 0.0.0.0 
