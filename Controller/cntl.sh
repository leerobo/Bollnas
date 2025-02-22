export LOADTYPE="Controller" 
export PROMETHEUS_MULTIPROC_DIR="prometheus_multiproc_dir"
echo "Github Update"
git pull origin sensorhub
echo "Github API start "
fastapi dev mainController.py --port 14120 --host 0.0.0.0 