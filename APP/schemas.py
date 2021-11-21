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
        assert(len(v) > 50), "must have under 50 chars"
        return v

    @validator('email')
    def email_must_be_under_50_chars(cls, v):
        assert(len(v) > 50), "must have under 50 chars"
        return v

    @validator('message')
    def message_must_be_under_50_chars(cls, v):
        assert(len(v) > 50), "must have under 50 chars"
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
