from pydantic import BaseModel

class Post(BaseModel):
    username: str
    text: str
    imageurl: str