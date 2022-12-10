from pydantic import BaseModel

class Participant(BaseModel):
    account_id: int

    class Config:
        orm_mode = True

class UpdateParticipant(Participant):
    permissions: int

# Event schemas

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
    participants: list[Participant] = []

    class Config:
        orm_mode = True

class MyEvents(BaseModel):
    title: str
    description: str
    is_public: bool
    id: int

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