from pydantic import BaseModel,Field
from datetime import datetime
class LoginStruct(BaseModel):
    username: str = Field(serialization_alias = "_id")
    password: str

class RegisterStruct(BaseModel):
    username: str = Field(serialization_alias = "_id")
    password: str

class MongoUsersStruct(BaseModel):
    username: str = Field(serialization_alias = "_id")
    hashed_password: str
    scope: str

class TokenStruct(BaseModel):
    exp: datetime
    username: str
    token_type: str

    