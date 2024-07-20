from fastapi import APIRouter, Response, status
from ..config.db import connection
from ..schemas import postEntity, postsEntity
from ..models.post import Post


from bson import ObjectId 

router = APIRouter(prefix='/posts')

@router.get('')
def get_posts():
    return postsEntity(connection.local.post.find())


@router.get('/{id}')
def get_post(id: str):
    data = connection.local.post.find_one({"_id": ObjectId(id)})
    return postEntity(data)



@router.post('')
def create_post(post: Post):
    new_post = dict(post)

    id = connection.local.post.insert_one(new_post).inserted_id
    
    data = connection.local.post.find_one({"_id": id})
    
    return postEntity(data)




@router.get('/user/{username}')
def get_posts_of_user(username: str):
    return f'hello {username}'

@router.put('/{id}')
def update_post(id: int):
    return f'hello {id}'

@router.delete('/{id}') 
def delete_post(id: str):
    connection.local.post.find_one_and_delete({"_id": ObjectId(id)})
    return Response(status_code=status.HTTP_204_NO_CONTENT)