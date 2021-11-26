from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserSignUp, LoginForm
from ..hashing import Hash
from ..token import create_access_token
from .. import models

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
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


@router.post("/login")
def login(login_req: LoginForm, db: Session = Depends(get_db)):
    query = db.query(models.User).\
        filter(models.User.email == login_req.email).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify_password(login_req.password, query.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={"sub": login_req.email})
    return {"access_token": access_token, "token_type": "bearer"}
