"""
Database Configuration Script

This script sets up the database connection and configuration using SQLAlchemy.
It includes functions and utilities for managing database sessions and models.

Modules:
    - sqlalchemy: Core library for database connection and ORM.
    - dotenv: For loading environment variables from a .env file.
    - os: For accessing environment variables and system operations.

Key Components:
    - `get_db`: Provides a scoped database session.
    - `Base`: Declarative base class for database models.
    - `engine`: Database engine for connecting to the specified database.
    - `SessionLocal`: Session factory for creating session instances.
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

def get_db():
    """
    Provides a database session for use within a scoped context.
    
    This function is designed to be used with dependency injection or 
    as a context manager to ensure that database resources are properly 
    managed and closed after use.

    Yields:
        db (Session): An instance of a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------------------------
# Environment Variable Loading
# -----------------------------------------------------

# Load environment variables from .env file
load_dotenv(".env")

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# -----------------------------------------------------
# SQLAlchemy Engine Setup
# -----------------------------------------------------

# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)

# -----------------------------------------------------
# Declarative Base Setup
# -----------------------------------------------------

# Base class for declarative models
Base = declarative.declarative_base()

# -----------------------------------------------------
# Session Factory Setup
# -----------------------------------------------------

# `autocommit=False` ensures explicit transaction management
# `autoflush=False` avoids automatic flushes to the database
# SessionLocal for database operations
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)