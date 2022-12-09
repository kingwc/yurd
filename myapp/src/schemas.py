from pydantic import BaseModel

class AccountBase(BaseModel):
    email: str
    username: str

class AccountCreate(AccountBase):
    password: str

class Account(AccountBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True