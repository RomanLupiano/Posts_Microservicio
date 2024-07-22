from fastapi import APIRouter, Response, status, File, UploadFile, HTTPException
from ..database import database, Post, Like
from ..schemas import PostResponseModel, PostRequestModel

from typing import List

POST_LIMIT = 50

router = APIRouter(prefix='/posts')

@router.get("", response_model=List[PostResponseModel])
async def get_all_posts(page: int = 1, limit: int = 10):

    if page <= 0 or limit <= 0:
        raise HTTPException(400, 'Params must be greater than zero')
    
    if limit > POST_LIMIT:
        raise HTTPException(400, 'Retreive less posts at the same time')

    posts = Post.select().order_by(Post.created_at.desc()).paginate(page, limit)
    
    return [ post for post in posts]
    

@router.post('', response_model=PostResponseModel)
async def create_post(post: PostRequestModel):
    new_post = Post.create(username=post.username, 
                           text=post.text, 
                           imageurl="todo")
    return new_post


@router.get('/{id}', response_model=PostResponseModel)
async def get_post(id: str):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
        
    return post

@router.put('/{id}', response_model=PostResponseModel)
async def update_post(id: int, post_req: PostRequestModel):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    post.text = post_req.text
    post.imageurl = "modificado"
    
    post.save()
    
    return post
     
@router.delete('/{id}', response_model=PostResponseModel) 
async def delete_post(id: str):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    post.delete_instance()
    
    return post

@router.get('/user/{username}', response_model=List[PostResponseModel])
async def get_posts_of_user(username: str, page: int = 1, limit: int = 10):

    if page <= 0 or limit <= 0:
        raise HTTPException(400, 'Params must be greater than zero')
    
    if limit > POST_LIMIT:
        raise HTTPException(400, 'Retreive less posts at the same time')

    posts = Post.select().where(Post.username == username).order_by(Post.created_at.desc()).paginate(page, limit)
    
    return [ post for post in posts]



@router.get("/following/all", response_model=List[PostResponseModel])
async def get_posts_following(page: int = 1, limit: int = 10):

    if page <= 0 or limit <= 0:
        raise HTTPException(400, 'Params must be greater than zero')
    
    if limit > POST_LIMIT:
        raise HTTPException(400, 'Retreive less posts at the same time')

    usernames = ['Manolo', 'Roman', 'Valentina']

    posts = Post.select().where(Post.username.in_(usernames)).order_by(Post.created_at.desc()).paginate(page, limit)
    
    return [post for post in posts]
