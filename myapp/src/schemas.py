from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    description: str | None = None
    is_public: bool

class EventCreate(EventBase):
    # to inherit EventBase
    pass

class Event(EventBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

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