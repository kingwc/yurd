from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, DateTime
import datetime
from .database import Base

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
    date_joined = Column(DateTime)

    #relation
    events = relationship('Event', back_populates='owner')



class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, default=None)
    owner_id = Column(Integer, ForeignKey('accounts.id'))
    is_public = Column(Boolean, default=False)
    date_created = Column(DateTime)
    hub_id = Column(Integer, default=None)

    #relation
    owner = relationship('Account', back_populates='events')