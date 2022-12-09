import sys
sys.path.append("..")

from sqlalchemy import delete
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

###################
# Create functions
###################

def create_account(db: Session, account: schemas.AccountCreate):
    hashed_password = get_password_hash(account.password)
    db_account = models.Account(
        username=account.username, 
        email=account.email, 
        hashed_password=hashed_password,
        first_name=account.first_name,
        last_name=account.last_name)

    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        title=event.title,
        description=event.description,
        is_public=event.is_public,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


#################
# Read functions
#################

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()

def get_account_by_username(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()

# Query 10 accounts
def get_accounts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Account).offset(skip).limit(limit).all()

################
# Test functions
################

