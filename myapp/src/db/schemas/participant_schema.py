from pydantic import BaseModel

class Participant(BaseModel):
    account_id: int

    class Config:
        orm_mode = True

class UpdateParticipant(Participant):
    permissions: int