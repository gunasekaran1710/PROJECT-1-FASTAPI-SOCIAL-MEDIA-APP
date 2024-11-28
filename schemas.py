from pydantic import BaseModel
from datetime import datetime
class users(BaseModel):
    email:str
    name:str
    password:str
class user_out(BaseModel):
    id:int
    name:str
    email:str
class loginUser(BaseModel):
    email:str
    password:str
class assessToken(BaseModel):
    access_token:str
    token_type:str
class token(BaseModel):
    token:str
class userNameChange(BaseModel):
    new_userName:str
class createPost(BaseModel):
    title:str
    content:str
class postOut(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime
    owner_id:int
class Votes(BaseModel):
    direction:int
    post_id:int
class postCreation(BaseModel):
    post:postOut
    owner:user_out
class postWithUserVote(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime
    owner_id:int
    owner_email:str
    owner_name:str
    votes:int
class postUpdate(BaseModel):
    title:str
    content:str

   
    
    

