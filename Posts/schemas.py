from typing import Any
from pydantic import BaseModel
from datetime import datetime

class PostResponseModel(BaseModel):
    username: str
    text: str
    imageurl: str
    created_at: datetime
    
class PostRequestModel(BaseModel):
    username: str
    text: str
