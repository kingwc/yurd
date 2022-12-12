import sys
sys.path.append("..")
import secrets

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

def create_event(db: Session, event: schemas.EventCreate, account_id: int):
    db_event = models.Event(
        title=event.title,
        description=event.description,
        is_public=event.is_public,
        owner_id=account_id,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def add_participant(db: Session, event_id: int, account_id: int):
    db_participant = models.Participant(
        event_id = event_id,
        account_id = account_id
    )

    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def add_invite(
        db: Session, 
        account_id_received: int,
        account_id_sent: int,
        event_id: int, 
        is_perm: bool
    ):

    code = secrets.token_urlsafe(5)
    i = 0
    while i < 10:
        try:
            get_invite_from_code(db=db, code=code)
            break
        except:
            code = secrets.token_urlsafe(5)
            i += 1
            continue

    db_invite = models.Invite(
        account_id_received=account_id_received,
        account_id_sent=account_id_sent,
        event_id=event_id,
        is_perm=is_perm
    )
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite

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

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_participant(db: Session, account_id: int):
    return db.query(models.Participant).filter(models.Participant.account_id == account_id).first()

def get_invite_from_code(db: Session, code: str):
    return db.query(models.Participant).filter(models.Participant.code == code).first()

def test_invite_exists(db: Session, account_id_received: int, event_id: int):
    return db.query(models.Participant).filter(
        models.Participant.account_id_received == account_id_received and models.Participant.event_id == event_id).first()

def get_invites_from_account_id(db: Session, account_id: int):
    return db.query(models.Invite).filter(models.Invite.account_id_received == account_id).all()

################
# Test functions
################

