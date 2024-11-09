from typing import Any, List
import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

from datetime import datetime

router = APIRouter()

logger = logging.getLogger("fastapi")
from sqlalchemy.ext.asyncio import AsyncSession

@router.post("/")
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user_in.created_at = datetime.now()
    user = crud.user.create(db, obj_in=user_in)
    
    return user

@router.put("/")
def update_user(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    data: schemas.UserUpdate = None
) -> Any:
    if current_user.status == "inactive" or current_user.user_type == "client":
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )  
    db_obj = crud.user.get(db=db, id=id)
    updated_at = datetime.now()
    data.updated_at = updated_at
    user = crud.user.update(db=db, db_obj=db_obj, obj_in=data)
    return user

@router.delete("/")
def delete(    
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):
    if current_user.status == "inactive" or current_user.user_type == "client":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access",
        )  
    obj = crud.user.remove(db=db, id=id)
    return obj

@router.get("/users/")
def list_users(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    if current_user.status == "inactive" or current_user.user_type == "client":
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )  
    return crud.user.get_multi(db=db)

@router.get("/clients/")
def list_clients(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    if current_user.status == "inactive" or current_user.user_type == "client" :
        raise HTTPException(
            status_code=401,
            detail="Unauthorized access",
        )  
    return crud.user.get_clients(db=db)