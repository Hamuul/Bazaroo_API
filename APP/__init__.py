from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from APP.routers import (
                        contact_requests,
                        users,
                        auth,
                        reviews,
                        tutoring_classes,)

from APP.database import engine
from APP import models


models.Base.metadata.create_all(engine)


def create_app():
    app = FastAPI()
    app.include_router(contact_requests.router,
                       prefix="/contact-request",
                       tags=['Contact Requests'])
    app.include_router(users.router, prefix="/users", tags=['Users'])
    app.include_router(auth.router, prefix="/auth", tags=['Users'])
    app.include_router(reviews.router, prefix="/reviews", tags=['Reviews'])
    app.include_router(tutoring_classes.router, prefix="/tutoring-classes",
                       tags=['Tutoring Classes'])

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    return app
