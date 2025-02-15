import requests
import os

def getrequest(path:str, payload:dict):
    response = requests.get(os.getenv("INTERNALROUTERPATH")+f"/{path}",params=payload)
    return response.json()

def postrequest(path:str, payload:dict):
    response = requests.post(os.getenv("INTERNALROUTERPATH")+f"/{path}",json=payload)
    return response.json()