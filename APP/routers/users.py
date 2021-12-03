from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from APP.schemas import UserShow, UserUpdate
from APP.database import get_db
from APP.hashing import Hash
from APP import models

router = APIRouter()


@router.get("/", response_model=List[UserShow])
def get_all_users(db: Session = Depends(get_db)):
    response = db.query(models.User).all()
    return response


@router.get("/{id}", response_model=UserShow)
def get_user_by_id(id, db: Session = Depends(get_db)):
    req = db.query(models.User).filter(models.User.id == id).first()
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return req


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id, req: UserUpdate, db: Session = Depends(get_db)):
    old_user = db.query(models.User).filter(models.User.id == id).first()
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if req.firstname is not None:
        old_user.firstname = req.firstname
    if req.lastname is not None:
        old_user.lastname = req.lastname
    if req.email is not None:
        if req.email.endswith('@stud.upb.ro') and old_user.role == 'student':
            old_user.email = req.email
        if req.email.endswith('@onmicrosoft.upb.ro') and old_user.role == 'teacher':
            old_user.email = req.email
    if req.password is not None and req.password == req.confirmation_password:
        old_user.password = Hash.bcrypt(req.password)
    db.commit()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_user(id, db: Session = Depends(get_db)):
    req = db.query(models.User).filter(models.User.id == id).first()
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.User).filter(models.User.id == id).\
        delete(synchronize_session=False)
    db.commit()
