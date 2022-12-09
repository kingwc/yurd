import sys
sys.path.append('..')
from fastapi import FastAPI

from . import models
from .database import engine
from src.APILoginController import APILoginApp

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/login", APILoginApp)