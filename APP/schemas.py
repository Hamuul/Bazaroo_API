from pydantic import (BaseModel,
                      EmailStr,
                      StrictBool,
                      StrictStr,
                      StrictInt,
                      validator)

from typing import Optional


class ContactRequestIn(BaseModel):
    message: StrictStr
    name: StrictStr
    email: EmailStr

    @validator('name')
    def name_must_be_under_50_chars(cls, v):
        assert(len(v) < 50), "must have under 50 chars"
        return v

    @validator('email')
    def email_must_be_under_50_chars(cls, v):
        assert(len(v) < 50), "must have under 50 chars"
        return v

    @validator('message')
    def message_must_be_under_50_chars(cls, v):
        assert(len(v) < 50), "must have under 50 chars"
        return v

    class Config:
        orm_mode = True


class ContactRequestOut(BaseModel):
    id: Optional[StrictInt]
    message: Optional[StrictStr]
    name: Optional[StrictStr]
    email: Optional[EmailStr]
    is_resolved: StrictBool

    class Config:
        orm_mode = True


class UserShow(BaseModel):
    id: Optional[StrictInt]
    email: Optional[EmailStr]
    firstname: Optional[StrictStr]
    lastname: Optional[StrictStr]
    role: Optional[StrictStr]

    @validator('lastname')
    def lastname_must_be_under_50_chars(cls, v):
        assert(len(v) < 50), 'must have under 50 chars'
        return v

    @validator('firstname')
    def firstname_must_be_under_50_chars(cls, v):
        assert(len(v) < 50), 'must have under 50 chars'
        return v

    @validator('role')
    def member(cls, v):
        assert(v in ['student', 'teacher']), 'must be student or teacher'
        return v

    class Config:
        orm_mode = True


class UserSignUp(UserShow):
    password: StrictStr
    confirmation_password: StrictStr

    @validator('password')
    def pass_between_8_and_50_chars(cls, v):
        assert(len(v) < 50 and len(v) > 8), 'must have between 8 and 50 chars'
        return v

    @validator('confirmation_password')
    def confpass_between_8_and_50_chars(cls, v):
        assert(len(v) < 50 and len(v) > 8), 'must have between 8 and 50 chars'
        return v
