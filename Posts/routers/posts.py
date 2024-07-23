from fastapi import APIRouter, Response, status, Form, File, UploadFile, HTTPException, Depends
from ..database import database, Post, Like
from ..schemas import PostResponseModel, PostRequestModel, LikeDetail, LikeResponse
from ..storage import upload_image
from ..tokens import decode_jwt, oauth2_scheme, InvalidTokenError, ExpiredTokenError

from typing import List

import httpx

POST_LIMIT = 50

router = APIRouter(prefix='/api/v1/posts')

@router.get("", response_model=List[PostResponseModel])
async def get_all_posts(page: int = 1, limit: int = 10):

    if page <= 0 or limit <= 0:
        raise HTTPException(400, 'Params must be greater than zero')
    
    if limit > POST_LIMIT:
        raise HTTPException(400, 'Retreive less posts at the same time')

    posts = Post.select().order_by(Post.created_at.desc()).paginate(page, limit)
    
    return [ post for post in posts]
    

@router.post('', response_model=PostResponseModel)
async def create_post(text: str = Form(...), image: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    
    try:
        username = decode_jwt(token)
        
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    try:
        image_url = upload_image(image)
        
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
async def update_post(id: int, text: str | None = Form(None), image: UploadFile | None = File(None), token: str = Depends(oauth2_scheme)):
    if text is None and image is None:
        raise HTTPException(status_code=400, detail="Nothing to modify")

    try:
        username = decode_jwt(token)
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    post = Post.select().where(Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')

    if post.username != username: 
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    if image is not None:
        try:
            image_url = upload_image(image)
            post.imageurl = image_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")

    if text is not None:
        post.text = text

    post.save()

    return post
    
     
@router.delete('/{id}', response_model=PostResponseModel) 
async def delete_post(id: str, token: str = Depends(oauth2_scheme)):
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    try:
        username = decode_jwt(token)
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    if post.username != username:
        raise HTTPException(401, "Not your post")    
        
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
async def get_posts_following(page: int = 1, limit: int = 10, token: str = Depends(oauth2_scheme)):

    if page <= 0 or limit <= 0:
        raise HTTPException(400, 'Params must be greater than zero')
    
    if limit > POST_LIMIT:
        raise HTTPException(400, 'Retreive less posts at the same time')
    
    try:
        username = decode_jwt(token)
        
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    
    following_users = await get_following_users(username)

    if not following_users:
        raise HTTPException(404, "You must follow at least one user to search posts")
    
    usernames = [item['username'] for item in following_users]
    
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
async def post_like(id: str, token: str = Depends(oauth2_scheme)):
    try:
        username = decode_jwt(token)
        
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    like, created = Like.get_or_create(post=post, username=username)
    
    if not created:
        raise HTTPException(409, "Already liked")
    
    return Response("Liked", status_code=status.HTTP_200_OK)


@router.delete('/{id}/like') 
async def delete_like(id: str, token: str = Depends(oauth2_scheme)):
    try:
        username = decode_jwt(token)
        
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    
    post = Post.select().where(Post.id == id).first()
    
    if post is None:
        raise HTTPException(404, 'Post not found')
    
    like = Like.select().where((Like.post == post) & (Like.username == username)).first()
    
    if like is None:
        raise HTTPException(404, 'Like not found')
    
    like.delete_instance()
    
    return Response("Disliked", status_code=status.HTTP_200_OK)



async def get_following_users(username: str):
    async with httpx.AsyncClient() as client:
        url = f"http://127.0.0.1:8000/api/v1/profile/{username}/following"
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching following users")
        return response.json()
    
    