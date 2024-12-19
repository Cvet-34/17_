from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import relationship
from app.models import *


class Task(Base):
    __tablename__='tasks'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True) #primary_key=True данный столбец будет представлять первичный ключ, index=True для этого столбца будет создаваться индекс.
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    sulg = Column(String, unique=True, index=True)


    user = relationship('User', back_populates='tasks')


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))










































