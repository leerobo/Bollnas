################# Bollnas ######### 14121 ##########
FROM python:3.12.2-slim-bookworm

# Controller
EXPOSE 14121   
#ENV YOURAPPLICATION_SETTINGS=/config.py 
#ENV PYTHONPATH=/Models

# Install pip requirements
WORKDIR /app
COPY /requirements.txt .
COPY /README.md .
RUN python3 -m pip install -r /app/requirements.txt --no-cache-dir

# Package up Folders 
WORKDIR /app
COPY Bollnas         /app/Bollnas

WORKDIR /app
# Run Controller 
CMD ["gunicorn","-w","4","-b","0.0.0.0:444", "app:create_app()"]
# Run sensorHub