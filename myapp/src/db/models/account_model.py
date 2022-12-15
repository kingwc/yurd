from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
import datetime
from src.db.database_connection import Base
import time
from src.db.database_connection import Base

# Models

class Account(Base):
    # Name of table
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    date_joined = Column(String, default=datetime.datetime.now())

    #relation
    events = relationship('Event', back_populates='owner')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, default=None)
    owner_id = Column(Integer, ForeignKey('accounts.id'))
    is_public = Column(Boolean, default=False)
    date_created = Column(String, default=datetime.datetime.now())
    hub_id = Column(Integer, default=None)

    #relation
    participants = relationship('Participant', back_populates='events')
    owner = relationship('Account', back_populates='events')

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    permission = Column(Integer, default=1)
    
    events = relationship('Event', back_populates='participants')

class Invite(Base):
    __tablename__ = 'invites'

    id = Column(Integer, primary_key=True, index=True)
    account_id_received = Column(Integer, ForeignKey('accounts.id'))
    account_id_sent = Column(Integer, ForeignKey('accounts.id'))
    event_id = Column(Integer)
    code = Column(Integer, unique=True)
    is_perm = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)
