from typing import Optional
from passlib.context import CryptContext

from src.structs import LoginStruct, MongoUsersStruct, RegisterStruct
from src.router import postrequest

def login(login_info:LoginStruct, pwd_context: CryptContext) -> MongoUsersStruct|bool|None:
    response = postrequest("mongo",
                           {"db":"Penguin",
                            "collection":"users",
                            "operation":"find_one",
                            "data":{"_id":login_info.username}
                            }
                        )
    
    if response != None:
        user_data = MongoUsersStruct(
            username=response["_id"],
            hashed_password=response["hashed_password"],
            scope=response["scope"]
        )   
        if pwd_context.verify(login_info.password,user_data.hashed_password):
            return user_data
        else:
            return False
    else:
        return None

def registration(register_info:RegisterStruct, pwd_context: CryptContext) -> dict:
    hashed_password = pwd_context.hash(register_info.password)
    payload = MongoUsersStruct(
        username = register_info.username,
        hashed_password = hashed_password,
        scope = ""
    )
    
    response = postrequest("mongo",
                           {"db":"Penguin",
                            "collection":"users",
                            "operation":"insert_one",
                            "data":payload.model_dump(by_alias=True)
                            }
                        )
    return response