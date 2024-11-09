from sqlalchemy import Column, Integer, String, Enum, DECIMAL, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from app.db.base_class import Base

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashedPassword = Column(String, nullable=False)
    user_type = Column(Enum('admin', 'base', name='user_types'), default='client')
    status = Column(Enum('active', 'inactive', name='user_status'), default='active')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)