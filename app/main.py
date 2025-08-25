from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, auth, space, booking
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(space.router)
app.include_router(booking.router)