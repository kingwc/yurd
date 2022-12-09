import sys
sys.path.append('..')
from fastapi import FastAPI

from src import models
from src.database import engine
from src.APIAccountsController import APIAccountsApp

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/accounts", APIAccountsApp)