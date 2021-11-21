from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from ..schemas import UserShow
from ..database import get_db
from .. import models

router = APIRouter()


@router.get("/users", response_model=List[UserShow])
def get_all_users(db: Session = Depends(get_db)):
    response = db.query(models.User).all()
    return response


@router.get("/users/{id}", response_model=UserShow)
def get_user_by_id(id, db: Session = Depends(get_db)):
    req = db.query(models.User).filter(models.User.id == id).first()
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return req
