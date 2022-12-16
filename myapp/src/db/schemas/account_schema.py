from pydantic import BaseModel
from src.db.schemas.event_schema import Event

# Acount schemas

class AccountBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str

class AccountCreate(AccountBase):
    password: str

class Account(AccountBase):
    id: int
    is_active: bool
    events: list[Event] = []

    class Config:
        orm_mode = True

