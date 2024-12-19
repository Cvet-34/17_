from fastapi import APIRouter, Depends, status, HTTPException  # обеспечивает взаимосвязи, зависимостями,
                                                                # устанавливаeт статусы и обрабатывает ошибки
from sqlalchemy.orm import Session                  #БД Сессия
from app.backend.db_depends import get_db           #Функция подкулючения к базе данных
from typing import Annotated                        #Аннотации

from app.models import *                            # импорт из model

from app.schemas import CreateTask, UpdateTask         # Модели базы данных

from slugify import slugify                 # функция slug строки

router = APIRouter(prefix="/task", tags=["task"])

# функции работы с записями
from sqlalchemy import select, delete
from sqlalchemy import update
from sqlalchemy import insert


@router.get('/')                    #описывает маршрут для получения задачи по её идентификатору
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task)).all()
    return task


@router.get('/task_id')  #описывает маршрут для получения задачи по её идентификатору
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    try:
        task = db.scalars(select(Task).where(Task.id == task_id))
        return task
    except IndexError:
        raise HTTPException(status_code=404, detail='Message Not found')


@router.post('/create')  #это определение маршрута обработки HTTP-запроса POST по указанному пути в приложении Express
async def create_task(db: Annotated[Session, Depends(get_db)], create_task_: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User wes not fond")

    db.execute(insert(Task).values(
                                title=create_task_.title,       # values подстваляем в табличку Task значение username и тд.
                                content=create_task_.content,
                                priority=create_task_.priority,
                                user_id=user_id,
                                slag=slugify(create_task_.title)))           #slag при помощи библиотеки slugify
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task_: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(
                                    firstname=update_task_.firstname,  # values подстваляем в табличку Task значение username и тд.
                                    lastname=update_task_.lastname,
                                    age=update_task_.age,
                                    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Task update is successful'
    }


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    user = db.scalar(select(Task).where(Task.id == task_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User is task found'
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }