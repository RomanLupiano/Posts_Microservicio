from fastapi import APIRouter, Response, status, Form, File, UploadFile, HTTPException
from ..database import database, Post, Like
from ..schemas import PostResponseModel, PostRequestModel, LikeDetail, LikeResponse
from ..storage import bucket

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
async def create_post(username: str = Form(...), text: str = Form(...), image: UploadFile = File(...)):
    
    try:
        blob = bucket.blob(image.filename)
        blob.upload_from_file(image.file, content_type=image.content_type)
        image_url = blob.public_url
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")

    
    post_data = PostRequestModel(username=username, text=text)
    
    new_post = Post.create(username=post_data.username, 
                           text=post_data.text, 
                           imageurl=image_url)
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



@router.get('/{id}/like', response_model=LikeResponse) 
async def get_likes(id: str):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    like_count = post.likes.count()
    
    likes = Like.select(Like.username, Like.created_at).where(Like.post == post)
        
    like_details = [LikeDetail(username=like.username, created_at=like.created_at) for like in likes]
    
    return LikeResponse(like_count=like_count, likes=like_details)


@router.post('/{id}/like') 
async def post_like(id: str):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    like, created = Like.get_or_create(post=post, username='Manolo')
    
    if not created:
        raise HTTPException(409, "Already liked")
    
    return Response("Liked", status_code=status.HTTP_200_OK)


@router.delete('/{id}/like') 
async def delete_like(id: str):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    like = Like.select().where((Like.post == post) & (Like.username == "Manolo")).first()
    
    if like is None:
        raise HTTPException(404, 'Like not found')
    
    like.delete_instance()
    
    return Response("Disliked", status_code=status.HTTP_200_OK)