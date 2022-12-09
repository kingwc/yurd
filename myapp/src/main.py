from fastapi import FastAPI
from pydantic import BaseModel
from src.APILoginController import APILoginApp

app = FastAPI()
app.mount("/login", APILoginApp)