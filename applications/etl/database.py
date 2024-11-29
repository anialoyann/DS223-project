from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (ensure this matches the one in docker-compose.yml)
DATABASE_URL = "postgresql://username:password@db:5432/mydatabase"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()
