FROM python:3.12-slim AS dev

# Controller
EXPOSE 14120  
 
# Install pip requirements
WORKDIR /Bollnas
COPY /pyproject.toml .
COPY /requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir  

# Package up Folders 
COPY /README.md    /Bollnas
COPY /Controller   /Bollnas/Controller
COPY /Common       /Bollnas/Common

WORKDIR /Bollnas/Controller

#CMD ["uvicorn", "--host", "0.0.0.0", "--port","14121","mainSensorhub.py", "--reload"]
CMD ["fastapi","dev","mainController.py","--port","14120","--host","0.0.0.0"]
