from pydantic import (BaseModel,
                      EmailStr,
                      StrictBool,
                      StrictInt,
                      validator,
                      constr)

from typing import Optional
from fastapi import HTTPException, status


class ContactRequestIn(BaseModel):
    message: constr(strict=True, max_length=5000)
    name: constr(strict=True, max_length=50)
    email: EmailStr

    class Config:
        orm_mode = True

    @validator('email')
    def email_under_50_chars(cls, v):
        if len(v) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='email must be no longer than 50 chars')
        return v


class ContactRequestOut(BaseModel):
    id: Optional[StrictInt]
    message: Optional[constr(strict=True, max_length=5000)]
    name: Optional[constr(strict=True, max_length=50)]
    email: Optional[EmailStr]
    is_resolved: StrictBool

    class Config:
        orm_mode = True

    @validator('email')
    def email_under_50_chars(cls, v):
        if len(v) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='email must be no longer than 50 chars')
        return v


class UserShow(BaseModel):
    id: Optional[StrictInt]
    email: Optional[EmailStr]
    firstname:  constr(strict=True, max_length=50)
    lastname: constr(strict=True, max_length=50)
    role: constr(strict=True, max_length=7)

    class Config:
        orm_mode = True

    @validator('role')
    def member(cls, v):
        if (v not in ['student', 'teacher']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='must be student or teacher')
        return v

    @validator('email')
    def email_under_50_chars(cls, v):
        if len(v) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='email must be no longer than 50 chars')
        return v


class UserSignUp(UserShow):
    password: constr(strict=True, min_length=8, max_length=50)
    confirmation_password: constr(strict=True, min_length=8, max_length=50)


class UserUpdate(BaseModel):
    id: Optional[StrictInt]
    email: Optional[EmailStr]
    firstname: Optional[constr(strict=True, max_length=50)]
    lastname: Optional[constr(strict=True, max_length=50)]
    role: Optional[constr(strict=True, max_length=7)]
    password: Optional[constr(strict=True, min_length=8, max_length=50)]
    confirmation_password: Optional[constr(strict=True, min_length=8,
                                           max_length=50)]

    class Config:
        orm_mode = True

    @validator('role')
    def member(cls, v):
        assert(v in ['student', 'teacher']), 'must be student or teacher'
        return v

    @validator('email')
    def email_under_50_chars(cls, v):
        if len(v) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='email must be no longer than 50 chars')
        return v


class LoginForm(BaseModel):
    email: EmailStr
    password: constr(strict=True, min_length=8, max_length=50)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class Review(BaseModel):
    id: Optional[StrictInt]
    message: constr(strict=True, max_length=500)
    user_id: Optional[StrictInt]

    class Config:
        orm_mode = True


class ClassShow(BaseModel):
    id: StrictInt
    description: constr(strict=True, max_length=500)
    teacher_id: StrictInt
    subject: constr(strict=True, max_length=80)

    class Config:
        orm_mode = True


class ClassUpdate(BaseModel):
    description: constr(strict=True, max_length=500)

    class Config:
        orm_mode = True


class ClassCreate(ClassUpdate):
    subject: constr(strict=True, max_length=80)
