import jwt,datetime
from dotenv import load_dotenv
import os
load_dotenv()
from rest_framework.exceptions import AuthenticationFailed
class Token:
    sign_key = os.getenv("SECRET_JWT")
    @staticmethod
    def generateToken(payload):
        compact_jws = jwt.encode(payload, Token.sign_key, algorithm='HS256')
        return compact_jws

    @staticmethod
    def decodeToken(token):
        try:
            payload = jwt.decode(token, Token.sign_key, algorithms=["HS256"])
            return payload
        except:
            raise AuthenticationFailed("Unauthorized!")