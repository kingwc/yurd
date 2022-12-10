from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import get_db
from src.APIAccountsController import get_current_active_user

APIEventsApp = FastAPI()

@APIEventsApp.post('/create')
async def create_event(
        event: schemas.EventCreate, 
        db: Session = Depends(get_db),
        account: schemas.Account = Depends(get_current_active_user),
    ):
    print('test')
    return crud.create_event(db=db, event=event, account_id=account.id)

@APIEventsApp.get('/myevents')
async def my_events(account: schemas.Account = Depends(get_current_active_user)):
    events = account.events
    #convert to json
    return events

@APIEventsApp.get('/{event_id}')
async def event_query(event_id: int, db: Session = Depends(get_db)):
    return crud.get_event(db=db, event_id=event_id)

@APIEventsApp.post('/{event_id}/join')
async def join_event(
        event_id: int, 
        db: Session = Depends(get_db),
        account: schemas.Account = Depends(get_current_active_user)
        ):

    event = crud.get_event(db=db, event_id=event_id)
    if event.is_public is True:
        crud.add_participant(db=db, event_id=event_id, account_id=account.id)
    else:
        #todo check invite table for code
        raise HTTPException(status_code=401, detail="No permission to join event")