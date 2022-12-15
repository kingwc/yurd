# from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
import time
from ..database_connection import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('accounts.id'))

    #relation
    #owner = relationship('Account', back_populates='events')
