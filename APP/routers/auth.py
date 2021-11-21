from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserSignUp, UserShow
from ..hashing import Hash
from .. import models

router = APIRouter()


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def create_user(req: UserSignUp, db: Session = Depends(get_db)):
    valid_email = bool((
        req.role == 'student' and req.email.endswith("@stud.upb.ro"))
        or (req.role == 'teacher' and req.email.endswith("@onmicrosoft.upb.ro")))
    if not valid_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    new_user = models.User(firstname=req.firstname,
                           lastname=req.lastname, email=req.email,
                           password=Hash.bcrypt(req.password),
                           role=req.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 'User was created successfully'


@router.post("/auth/login", response_model=UserShow)
def login(db: Session = Depends(get_db)):
    pass
