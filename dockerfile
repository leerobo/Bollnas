################# VINCENT ######### 444 ##########
FROM python:3.12.2-slim-bookworm

EXPOSE 444
ENV YOURAPPLICATION_SETTINGS=/config.py 
ENV PYTHONPATH=/Models

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# FLASK_ENV set within compose

# ----- Production 
#ENV FLASK_DEBUG=0
#ENV FLASK_ENV=production
# ----- Cert (MTF)
#ENV FLASK_DEBUG=1
#ENV FLASK_ENV=MTF
# ----- Staged (Developement)
#ENV FLASK_DEBUG=1
#ENV FLASK_ENV=staged
# ----- Developement
#ENV FLASK_DEBUG=1
#ENV FLASK_ENV=development

# Install pip requirements
WORKDIR /VINcentAPP
COPY /requirements.txt .
COPY /README.md .
RUN python3 -m pip install -r /VINcentAPP/requirements.txt --no-cache-dir

# Package up Folders 
WORKDIR /VINcentAPP
COPY VINcent         /VINcentAPP/VINcent
COPY /SQL            /VINcentAPP/SQL
COPY /Models         /VINcentAPP/Models
COPY /DataStructures /VINcentAPP/DataStructures

# Dont upload Keys/config - These are server related
#RUN mkdir -p            /VINcentAPP/Config
#RUN mkdir -p            /VINcentAPP/Cert
#COPY /Config/readme.md  /VINcentAPP/Config
#COPY /Cert/readme.md    /VINcentAPP/Cert
RUN rm -rf /Cert/*


WORKDIR /VINcentAPP
CMD ["gunicorn","-w","4","-b","0.0.0.0:444", "VINcent:create_app()"]
