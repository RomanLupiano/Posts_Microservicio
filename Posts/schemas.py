from typing import Any
from pydantic import BaseModel
from datetime import datetime

class PostResponseModel(BaseModel):
    id: int
    username: str
    text: str
    imageurl: str
    created_at: datetime
    
class PostRequestModel(BaseModel):
    
    username: str
    text: str


class LikeDetail(BaseModel):
    username: str
    created_at: datetime

class LikeResponse(BaseModel):
    like_count: int
    likes: list[LikeDetail]