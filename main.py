import os
from fastapi import FastAPI, Request, HTTPException, Response
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

from passlib.context import CryptContext

from src.structs import LoginStruct, RegisterStruct, MongoUsersStruct
from src.authorization import UserManagement
from src.authentication import AccessToken

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR,'.env'))

app = FastAPI()

origins = [
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN = AccessToken()
USER_MANAGEMENT = UserManagement(PWD_CONTEXT)

@app.get("/")
async def root():
    return {"message":"Hello World","detail":"auth-server"}

@app.post("/login")
async def global_login(login_info: LoginStruct, response:Response):
    user_data = USER_MANAGEMENT.login(login_info)
    if user_data:
        token = ACCESS_TOKEN.create_token(user_data.username)
        response.set_cookie("auth_token",token,httponly=True)
        return {"message":"success"}
    elif user_data == None:
        raise HTTPException(400,{"message":"User Not Found"})
    else:
        raise HTTPException(400,{"message":"Wrong Credentials"})

@app.post("/refresh")
async def global_refresh(token_info):
    #check mongo sessions for username and verify refresh token
    #if true, assign new refresh token and bearer token
    #update the mongo sessions on new refresh token
    pass

@app.post("/credentials_authentication")
async def credentials_authentication(token:str):
    try:
        payload = ACCESS_TOKEN.decode_token(token)
        return payload
    except OSError:
        return HTTPException(401,{"message":"invalid JWT"})

@app.post("/register")
async def global_register(register_info: RegisterStruct):
    response = USER_MANAGEMENT.registration(register_info)
    return response
    