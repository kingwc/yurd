from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Change for production database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

# 'connect_args' for sqlite3 only, delete on production
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Class base used in models.py
Base = declarative_base()