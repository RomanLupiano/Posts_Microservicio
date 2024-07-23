from fastapi.security import OAuth2PasswordBearer
import jwt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"

class InvalidTokenError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        
class ExpiredTokenError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        
        if username is None:
            raise InvalidTokenError("Invalid token: missing data")
        
        return username
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError("Invalid token: Token has expired")
    except jwt.PyJWKError:
        raise InvalidTokenError("Invalid token: decoding error")

