from typing import Optional
from passlib.context import CryptContext

from src.structs import LoginStruct, MongoUsersStruct, RegisterStruct
from src.router import postrequest

class UserManagement:
    def __init__(self, pwd_context:CryptContext):
        self.pwd_context = pwd_context

    def login(self,login_info:LoginStruct) -> MongoUsersStruct|bool|None:
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
            if self.pwd_context.verify(login_info.password,user_data.hashed_password):
                return user_data
            else:
                return False
        else:
            return None

    def registration(self,register_info:RegisterStruct) -> dict:
        hashed_password = self.pwd_context.hash(register_info.password)
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