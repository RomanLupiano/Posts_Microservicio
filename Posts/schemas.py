def postEntity(item) -> dict:
    return {
        'username': item['username'],
        'text': item['text'],
        'imageurl': item['imageurl'],
    }
    
def postsEntity(entity) -> list:
    return [postEntity(item=item) for item in entity]