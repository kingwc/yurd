from pydantic import BaseModel
from src.db.schemas.participant_schema import Participant

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