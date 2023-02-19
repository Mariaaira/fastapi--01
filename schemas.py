# schemas是定义用于接口请求和响应的数据模型的工具。
# 使用schemas，可以确保相关数据被格式化正确，确保接口的安全和可靠性，还能够帮助开发者以及服务的消费者避免一些意外的bug。

# 数据被正确格式化

from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOuts(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

# Config类用于存储应用程序中整体配置信息。
# 因此，这段代码可能用于告诉应用程序尝试使用对象关系映射(ORM)来处理和存储数据库等操作。

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOuts

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


