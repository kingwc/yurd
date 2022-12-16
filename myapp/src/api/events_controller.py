from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.db.schemas import account_schema
from src.db.schemas.invite_schema import InviteCreate
from src.db.event_db import get_event, create_event
from src.db.invite_db import test_invite_exists, add_invite, get_invites_from_account_id
from src.db.participant_db import add_participant, get_participant
from src.db.schemas.event_schema import EventCreate
from src.db.database_connection import get_db
from src.api.accounts_controller import get_current_active_user

APIEventsApp = FastAPI()

# Create event (tied to account object under 'events')
@APIEventsApp.post('/create')
async def create_event(
        event: EventCreate, 
        db: Session = Depends(get_db),
        account: account_schema.Account = Depends(get_current_active_user),
    ):
    print('test')
    return create_event(db=db, event=event, account_id=account.id)

# Displays events under account object
@APIEventsApp.get('/myevents')
async def my_events(account: account_schema.Account = Depends(get_current_active_user)):
    events = account.events
    #TODO convert to json
    return events

# Queries event object of given event id
@APIEventsApp.get('/{event_id}')
async def event_query(event_id: int, db: Session = Depends(get_db)):
    return get_event(db=db, event_id=event_id)

# Join event based off event id and passing through account token
@APIEventsApp.post('/{event_id}/join')
async def join_event(
        event_id: int, 
        db: Session = Depends(get_db),
        account: account_schema.Account = Depends(get_current_active_user)
        ):
    # Checks if you have joined event already
    event = get_event(db=db, event_id=event_id)
    for i in account.events:
        if i.id == event.id:
            raise HTTPException(status_code=401, detail='You have already joined this event.')            
    # Checks if event is public
    if event.is_public is True:
        add_participant(db=db, event_id=event_id, account_id=account.id)
    else:
        #TODO check invite table for code
        raise HTTPException(status_code=401, detail="No permission to join event")

# Invite user to event via usernname (view schemas.InviteCreate for body query param)
@APIEventsApp.post('/invite')
async def create_invite(
    invite_info: InviteCreate,
    db: Session = Depends(get_db),
    account: account_schema.Account = Depends(get_current_active_user),
):
    # Check if user is already invited
    try:
        if test_invite_exists(
            db=db, 
            account_id_received=invite_info.account_id_received,
            event_id=invite_info.event_id
            ) is None:
            raise HTTPException(status_code=403, detail="You have already invited this user")
    except:
        raise HTTPException(status_code=403, detail="You have already invited this user")
    # Check if user inviting is participant of event
    try: 
        participant = get_participant()
    except:
        raise HTTPException(status_code=403, detail="You are not a part of this event")
    # Check participant permission (0 = cant invite, 1 = can invite, 2 = TODO)
    if participant.permission >= 1:
        add_invite(
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
    account: account_schema.Account = Depends(get_current_active_user),
):
    return get_invites_from_account_id(db=db, account_id=account.id)

#TODO accept_invite
# from code (url from text) or thru app query

#TODO delete_invite

