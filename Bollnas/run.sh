export CONTROLLER=True
export SENSORHUB=False
echo "Github Update"
#git pull origin sensorhub
echo "Github API start "
fastapi dev runapp.py --port 14121 --host 0.0.0.0 
