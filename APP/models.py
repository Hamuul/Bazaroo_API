from sqlalchemy import Column, Integer, String, Boolean


from .database import Base


class ContactRequest(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(length=5000))
    name = Column(String(length=50))
    email = Column(String(length=50), index=True)
    is_resolved = Column(Boolean, default=False, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(length=50))
    lastname = Column(String(length=50))
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String(length=256))
    role = Column(String(length=7))
