from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from APP.database import get_db
from APP.schemas import ClassUpdate, ClassShow, ClassCreate
from APP import models

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_class(req: ClassCreate, db: Session = Depends(get_db)):
    new_class = models.TutoringClass(description=req.description,
                                     subject=req.subject)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return 'Tutoring class created'


@router.get("/", response_model=List[ClassShow])
def get_all_classes(db: Session = Depends(get_db)):
    classes = db.query(models.TutoringClass).all()
    return classes


@router.delete("/{id}")
def del_class(id, db: Session = Depends(get_db)):
    d_class = db.query(models.TutoringClass).\
        filter(models.TutoringClass.id == id).first()
    if d_class is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.TutoringClass).\
        filter(models.TutoringClass.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Tutoring class removed'


@router.get("/{id}", response_model=ClassShow)
def get_class_by_id(id, req: ClassShow, db: Session = Depends(get_db)):
    needle = db.query(models.TutoringClass).\
        filter(models.TutoringClass.id == req.id).first()
    if needle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return needle


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_class(id, req: ClassUpdate, db: Session = Depends(get_db)):
    old_class = db.query(models.TutoringClass).\
        filter(models.TutoringClass.id == id).first()
    if old_class is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    old_class.description = req.description
    db.commit()
    return 'Tutoring class description updated'
    return 'Tutoring class description updated'


@router.post("/{id}/enroll", status_code=status.HTTP_201_CREATED)
def enroll_user(id, db: Session = Depends(get_db)):
    pass
