from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import get_db
from src.APIAccountsController import get_current_active_user

APIEventsApp = FastAPI()

# Create event (tied to account object under 'events')
@APIEventsApp.post('/create')
async def create_event(
        event: schemas.EventCreate, 
        db: Session = Depends(get_db),
        account: schemas.Account = Depends(get_current_active_user),
    ):
    print('test')
    return crud.create_event(db=db, event=event, account_id=account.id)

# Displays events under account object
@APIEventsApp.get('/myevents')
async def my_events(account: schemas.Account = Depends(get_current_active_user)):
    events = account.events
    #TODO convert to json
    return events

# Queries event object of given event id
@APIEventsApp.get('/{event_id}')
async def event_query(event_id: int, db: Session = Depends(get_db)):
    return crud.get_event(db=db, event_id=event_id)

# Join event based off event id and passing through account token
@APIEventsApp.post('/{event_id}/join')
async def join_event(
        event_id: int, 
        db: Session = Depends(get_db),
        account: schemas.Account = Depends(get_current_active_user)
        ):
    # Checks if you have joined event already
    event = crud.get_event(db=db, event_id=event_id)
    for i in account.events:
        if i.id == event.id:
            raise HTTPException(status_code=401, detail='You have already joined this event.')            
    # Checks if event is public
    if event.is_public is True:
        crud.add_participant(db=db, event_id=event_id, account_id=account.id)
    else:
        #TODO check invite table for code
        raise HTTPException(status_code=401, detail="No permission to join event")

# Invite user to event via usernname (view schemas.InviteCreate for body query param)
@APIEventsApp.post('/invite')
async def create_invite(
    invite_info: schemas.InviteCreate,
    db: Session = Depends(get_db),
    account: schemas.Account = Depends(get_current_active_user),
):
    # Check if user is already invited
    try:
        if crud.test_invite_exists(
            db=db, 
            account_id_received=invite_info.account_id_received,
            event_id=invite_info.event_id
            ) is None:
            raise HTTPException(status_code=403, detail="You have already invited this user")
    except:
        raise HTTPException(status_code=403, detail="You have already invited this user")
    # Check if user inviting is participant of event
    try: 
        participant = crud.get_participant()
    except:
        raise HTTPException(status_code=403, detail="You are not a part of this event")
    # Check participant permission (0 = cant invite, 1 = can invite, 2 = TODO)
    if participant.permission >= 1:
        crud.add_invite(
            db=db,
            account_id_received=invite_info.account_id_received,
            account_id_sent=account.id,
            event_id=invite_info.event_id,
            is_perm=invite_info.is_perm,
        )
    else:
        raise HTTPException(status_code=403, detail="You do not have permission to send invites")

# View all invites to account (no body param)
@APIEventsApp.get('/myinvites')
async def view_invites(
    db: Session = Depends(get_db),
    account: schemas.Account = Depends(get_current_active_user),
):
    return crud.get_invites_from_account_id(db=db, account_id=account.id)

#TODO accept_invite
# from code (url from text) or thru app query

#TODO delete_invite

