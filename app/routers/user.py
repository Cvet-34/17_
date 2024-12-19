from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert
from app.schemas import CreateUser, UpdateUser

from slugify import slugify

from sqlalchemy import select, delete
from sqlalchemy import update

router = APIRouter(prefix="/user", tags=["user"])


@router.get('/')
async def get_by_user(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    try:
        user = db.scalars(select(User).where(User.id == user_id))
        return user
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Message Not found")


@router.get('/user_id/tasks')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    db.scalars(select(Task).where(Task.user_id == user_id))
    return {"user_id": user.id, "tasks": [task for task in user.tasks]}


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)],
                      create_user_: CreateUser):  # values подстваляем в табличку значение username и тд.
    db.execute(insert(User).values(username=create_user_.username,
                                   firstname=create_user_.firstname,
                                   lastname=create_user_.lastname,
                                   age=create_user_.age,
                                   slug=slugify(create_user_.username)))  #slug при помощи библиотеки slugify
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def create_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,  # values подстваляем в табличку значение username и тд.
        lastname=update_user.lastname,
        age=update_user.age,
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is user found'
        )
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }
