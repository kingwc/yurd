from sqlalchemy.orm import Session

from src.db.models.participant_model import Participant

def add_participant(db: Session, event_id: int, account_id: int):
    db_participant = Participant(
        event_id = event_id,
        account_id = account_id
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participant(db: Session, account_id: int):
    return db.query(Participant).filter(Participant.account_id == account_id).first()