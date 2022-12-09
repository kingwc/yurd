from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

APILoginApp = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@APILoginApp.get("/items/")
async def login_read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}