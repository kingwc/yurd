from sqlalchemy.orm import Session

from src.db.schemas.event_schema import Event, EventCreate

def create_event(db: Session, event: EventCreate, account_id: int):
    db_event = Event(
        title=event.title,
        description=event.description,
        is_public=event.is_public,
        owner_id=account_id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()