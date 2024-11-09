from datetime import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.security import get_password_hash,verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.email == email, 
            self.model.status == "active"
        ).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)

        user_obj = self.model(
            name=obj_in.name,
            email=obj_in.email,
            user_type=obj_in.user_type,
            status=obj_in.status,
            created_at=datetime.now(),
            hashedPassword=hashed_password,
            updated_at=None
        )

        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)

        return user_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashedPassword):
           return None
        return user

    def get_clients(self, db: Session) -> Any:
        return db.query(User).filter(User.user_type == "client").all()
user = CRUDUser(User)