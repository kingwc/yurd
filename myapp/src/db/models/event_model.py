from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
import datetime
from src.db.database_connection import Base


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
