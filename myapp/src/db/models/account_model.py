# from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
import time
from ..database_connection import Base

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
    date_joined = Column(String, default=time.time())

