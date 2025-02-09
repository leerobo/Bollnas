FROM python:3.12-slim AS dev

# Sensorhub
EXPOSE 14121   
 
# Install pip requirements
WORKDIR /Bollnas
COPY /requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

RUN echo "work directory 1" > file1.txt

# Package up Folders 
COPY /README.md    /Bollnas
COPY /SensorHub    /Bollnas/SensorHub
COPY /Common       /Bollnas/Common
RUN pwd

WORKDIR /Bollnas/SensorHub
RUN echo "work directory 2" > file2.txt

#CMD ["uvicorn", "--host", "0.0.0.0", "--port","14121","mainSensorhub.py", "--reload"]
CMD ["fastapi","run","mainSensorhub.py","--port","14121","--host","0.0.0.0"]
