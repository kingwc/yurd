from pydantic import BaseModel

# Invite Schemas

class InviteCreate(BaseModel):
    account_id_received: int
    event_id: int 
    is_perm: bool

class InviteView(BaseModel):
    account_id: int