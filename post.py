from starlette.routing import Router
from typing import List, Optional
import schemas, models, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db
import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",  # + id --->  /posts/{id}
    tags=['Posts']
)
# tags用于添加分组标签，以便对RESTful API进行分类和组织。
# 它们可以帮助开发者快速找到特定API，有助于提高API查询效率，提高使用体验。


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db1: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # print(limit)
    posts = db1.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # .filter(models.Post.user_id == current_user.id).all()
    results = db1.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db1: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor = db.cursor()
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # db.commit()
    print(current_user)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db1.add(new_post)
    db1.commit()
    db1.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db1: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("select * from posts where id= %s", (str(id),))
    # post = cursor.fetchone()
    post = db1.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post with id {id} not found")

    #     return{'message':f'post with id: {id} was not found'}
    # return {"post_detail": post}
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db1: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("delete from posts where id=%s", (str(id),))
    # delete_post = cursor.fetchone()
    # db.commit()
    post_query = db1.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    # if delete_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    if post.user_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")

    post_query.delete(synchronize_session=False)
    db1.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db1: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("update posts set title = %s, content = %s, published = %s where id = %s", (updated_post.title, updated_post.content, updated_post.published, str(id)))
    # updated_post = cursor.fetchone()
    # db.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    #
    # return updated_post
    post_query = db1.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.user_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    post_query.update(updated_post.dict(), synchronize_session=False)

    db1.commit()
    return post_query.first()
