"""
Database Configuration
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(".env")

# Get the database URL from environment variables
DATABASE_URL = "postgresql://postgres:password@db:5432/ds223_gp_db"



# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)

# Base class for declarative models
Base = declarative.declarative_base()

# SessionLocal for database operations
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Function to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
