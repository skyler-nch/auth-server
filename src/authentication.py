import os
from jose import jwt, jwe

from datetime import datetime, timezone, timedelta
from src.structs import TokenStruct

class AccessToken:
    def __init__(self):
        self.algorithm = os.getenv("JWTALGO")
        self.secret = os.getenv("JWTSECRET")
        self.expiry_duration = int(os.getenv("JWTEXPIRYMINUTES"))
        self.encryption_secret=os.getenv("JWESECRET")

    def create_token(self, username:str):
        expiry_delta = datetime.now(timezone.utc) + timedelta(minutes=self.expiry_duration)
        token = TokenStruct(username=username,exp=expiry_delta,token_type="bearer")

        encoded_jwt = jwt.encode(token.model_dump(),self.secret,self.algorithm)
        encrypted_jwt = jwe.encrypt(encoded_jwt,self.encryption_secret,algorithm="dir",encryption="A128GCM")
        return encrypted_jwt.decode("UTF-8")
    
    def decode_token(self, token:str) -> dict:
        decrypted_json = jwe.decrypt(token.encode("UTF-8"),self.encryption_secret)
        decoded_json = jwt.decode(decrypted_json,self.secret,self.algorithm)
        return TokenStruct(**decoded_json)

