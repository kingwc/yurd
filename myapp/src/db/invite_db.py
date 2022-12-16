import secrets
from sqlalchemy.orm import Session

from src.db.models.participant_model import Participant
from src.db.models.invite_model import Invite

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

    db_invite = Invite(
        account_id_received=account_id_received,
        account_id_sent=account_id_sent,
        event_id=event_id,
        is_perm=is_perm
    )
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite

# Read functions

def get_invite_from_code(db: Session, code: str):
    return db.query(Invite).filter(Invite.code == code).first()

def test_invite_exists(db: Session, account_id_received: int, event_id: int):
    return db.query(Invite).filter(
        Invite.account_id_received == account_id_received and Participant.event_id == event_id).first()

def get_invites_from_account_id(db: Session, account_id: int):
    return db.query(Invite).filter(Invite.account_id_received == account_id).all()