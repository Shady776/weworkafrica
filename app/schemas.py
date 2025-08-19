from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass
class User(BaseModel):
    id: int
    email: EmailStr
    # password: str
    created_at: datetime
    
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: User
    
    class Config:
        orm_mode = True
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
    
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int