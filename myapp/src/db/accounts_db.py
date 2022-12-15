import sys

from sqlalchemy import delete
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Import Models
from src.db.models import account_model, event_model

# Import Schemas
from src.db.schemas import account_schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

###################
# Create functions
###################

def create_account(db: Session, account: account_schema.AccountCreate):
    hashed_password = get_password_hash(account.password)
    db_account = account_model.Account(
        username=account.username, 
        email=account.email, 
        hashed_password=hashed_password,
        first_name=account.first_name,
        last_name=account.last_name)

    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

#TODO def create_event

#################
# Read functions
#################

def get_account(db: Session, account_id: int):
    return db.query(account_model.Account).filter(account_model.Account.id == account_id).first()

def get_account_by_email(db: Session, email: str):
    return db.query(account_model.Account).filter(account_model.Account.email == email).first()

def get_account_by_username(db: Session, username: str):
    return db.query(account_model.Account).filter(account_model.Account.username == username).first()

# Query 10 accounts
def get_accounts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(account_model.Account).offset(skip).limit(limit).all()

################
# Test functions
################

