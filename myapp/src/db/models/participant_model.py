from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
import datetime
from src.db.database_connection import Base

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    permission = Column(Integer, default=1)
    
    events = relationship('Event', back_populates='participants')
