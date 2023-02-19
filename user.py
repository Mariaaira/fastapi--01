from starlette.routing import Router

import schemas, models, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db

router = APIRouter(
    prefix="/users",
    tags=['User']
)

# Response Model的作用是提供一种声明式的方式来定义API返回的响应。
# 这可以帮助你定义一个清晰的模式，并保证正确性和完整性，以确保API在不同状态下的行为一致。

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOuts)
def create_user(user: schemas.UserCreate, db1: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db1.add(new_user)
    db1.commit()
    db1.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOuts)
def get_user(id: int, db1: Session = Depends(get_db)):
    user = db1.query(models.User).filter(models.User.id == id).first()

    if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found")

    return user