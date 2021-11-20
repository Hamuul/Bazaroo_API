from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import StrictBool

from .schemas import ContactRequestOut, ContactRequestIn
from .database import engine, SessionLocal
from . import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app():
    app = FastAPI()

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    @app.post("/contact-requests", status_code=status.HTTP_201_CREATED)
    def create_req(req: ContactRequestIn, db: Session = Depends(get_db)):
        new_req = models.ContactRequest(name=req.name, message=req.message,
                                        email=req.email)
        db.add(new_req)
        db.commit()
        db.refresh(new_req)

    @ app.get("/contact-requests")
    def get_req(db: Session = Depends(get_db)):
        req = db.query(models.ContactRequest).all()
        return req

    @ app.get("/contact-requests/{id}", response_model=ContactRequestOut)
    def get_req_by_id(id, db: Session = Depends(get_db)):
        req = db.query(models.ContactRequest).filter(
            models.ContactRequest.id == id).first()
        if req is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Request with id {id} not found")
        return req

    @app.delete("/contact-requests/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def del_req(id, db: Session = Depends(get_db)):
        req = db.query(models.ContactRequest).filter(
            models.ContactRequest.id == id).first()
        if req is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Request with id {id} not found")
        else:
            db.query(models.ContactRequest).filter(
                models.ContactRequest.id == id).delete(synchronize_session=False)
            db.commit()
            return {"detail": f"request with id{id} was deleted"}

    @app.patch("/contacts-requests/{id}", status_code=status.HTTP_202_ACCEPTED)
    def update_req_status(id, req: ContactRequestOut, db: Session = Depends(get_db)):
        if type(req["is_resolved"]) is not StrictBool:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        find_req = db.query(models.ContactRequest).filter(
            models.ContactRequest.id == id).first()
        if find_req is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Request with id {id} not found")
        find_req.is_resolved = True
        db.commit()
        return {"detail": f"request with id {id} is now resolved"}
    return app
