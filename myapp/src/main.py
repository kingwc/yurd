from fastapi import FastAPI

from . import models
from .database import engine
from src.APILoginController import APILoginApp
from src.APIAccountCreateController import api_sign_up_app

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/login", APILoginApp)
app.mount('/signup', api_sign_up_app)