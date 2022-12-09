from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import get_db

APIEventsApp = FastAPI()

@APIEventsApp.post('/create')
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)