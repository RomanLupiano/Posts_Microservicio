from peewee import Model, SqliteDatabase, CharField, DateTimeField, ForeignKeyField
from datetime import datetime

database = SqliteDatabase('database.db')

class Post(Model):
    username = CharField()
    text = CharField()
    imageurl = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = database
        table_name = 'post'
        
class Like(Model):
    post = ForeignKeyField(Post, backref='likes', on_delete='CASCADE')  # Referencia al post
    username = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = database
        table_name = 'like'



database.connect()
database.create_tables([Post, Like])
