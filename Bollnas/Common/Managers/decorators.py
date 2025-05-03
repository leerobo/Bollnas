from functools import wraps
import base64, json, datetime, os
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi import HTTPException, status, Security
#from Bollnas.Common.zzzzzConfig import getConfig
from Common.ConfigLoad import getJSONconfig

# from jwcrypto import jws, jwk, jwt


def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs) -> tuple[object,int]:
        # TODO: Add JWT here or PEN validation
        print(kwargs,args)
        if getJSONconfig().Security.comms : 
           if getJSONconfig().Security.apikey != "" :
              if 'x_apikey' not in kwargs:
                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Missing ApiKey Header")
              if kwargs['x_apikey'] != getJSONconfig().Security.apikey :
                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid ApiKey Header")
              
           # if getJSONconfig().Security.pemCert != "" :
           # TODO : Setup JWT validation here 
           
        return await f(*args, **kwargs)
    return decorated
# 