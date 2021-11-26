from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import Review
from .. import models

router = APIRouter()


@router.get("/", response_model=List[Review])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(models.Review).all()
    return reviews


@router.get("/{id}", response_model=Review)
def get_review_by_id(id, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == id).first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return review


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_review(req: Review, db: Session = Depends(get_db)):

    new_review = models.Review(message=req.message, user_id=req.user_id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return 'Review created'


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_review(id, req: Review, db: Session = Depends(get_db)):
    old_review = db.query(models.Review).filter(models.Review.id == id).first()
    if old_review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    old_review.message = req.message
    db.commit()
    return f'Review {id} updated'


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_review(id, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == id).first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_Found)
    db.query(models.Review).filter(models.Review.id == id).\
        delete(synchronize_session=False)
    db.commit()
