from functools import wraps
import base64, json, datetime, os
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi import HTTPException, status, Security
from Common.Config import getConfig
# from jwcrypto import jws, jwk, jwt


def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs) -> tuple[object,int]:
        # TODO: Add JWT here or PEN validation
        print(kwargs,args)
        if len(getConfig().key) != 0 : 
           if 'x_apikey' not in kwargs:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Missing ApiKey Header")
           if kwargs['x_apikey'] == None:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Missing ApiKey")
           if kwargs['x_apikey'] not in getConfig().key :
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid ApiKey")        
        print('return dec')
        return await f(*args, **kwargs)
    return decorated

# 
    @wraps(f)
    def portalStatus(*args, **kwargs):
        try:
          if not current_app.config['PORTAL']  :  return '',404
        except:
          return '',404
        return f(*args, **kwargs)
    return portalStatus