from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
import datetime
from src.db.database_connection import Base

class Invite(Base):
    __tablename__ = 'invites'

    id = Column(Integer, primary_key=True, index=True)
    account_id_received = Column(Integer, ForeignKey('accounts.id'))
    account_id_sent = Column(Integer, ForeignKey('accounts.id'))
    event_id = Column(Integer)
    code = Column(Integer, unique=True)
    is_perm = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)