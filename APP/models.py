from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from APP.database import Base

enrolment_table = \
    Table('enrolment', Base.metadata,
          Column('tutoring_class_id', ForeignKey('tutoring_classes.id')),
          Column('user_id', ForeignKey('users.id')))


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
    firstname = Column(String(length=50), nullable=False)
    lastname = Column(String(length=50), nullable=False)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String(length=256))
    role = Column(String(length=7))

    review = relationship("Review")
    tutor = relationship("TutoringClass", secondary=enrolment_table)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(length=500), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class TutoringClass(Base):
    __tablename__ = "tutoring_classes"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(length=500))
    subject = Column(String(length=80))
    teacher_id = Column(Integer, ForeignKey("users.id"))
