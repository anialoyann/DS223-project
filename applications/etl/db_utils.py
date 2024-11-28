"""
Database Utilities Module

This module provides utility functions to interact with a database using SQLAlchemy. (although, this author is not very sure they're being used)
It includes functionality for inserting rows, deleting rows, and exporting data to a Pandas DataFrame.

Modules:
-----------------
- sqlalchemy: ORM for Python for database operations.
- pandas: For exporting and manipulating database data as DataFrames.
- psycopg2: PostgreSQL database adapter for Python (used internally by SQLAlchemy).
- dotenv: For loading environment variables from a .env file.
- time: For handling delays during retries.
- os: For accessing environment variables.

Environment Variables:
----------------------
- DATABASE_URL: A connection string to the database (loaded from the .env file).

Dependencies:
-------------
- AN .env file with the `DATABASE_URL` variable configured.
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import psycopg2
import time
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(".env")

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables.")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
Session = sessionmaker(bind=engine)


def insert_row(table, data, retries=5, delay=1):
    """
    Inserts a row into the specified table, with support for retries in case of unique constraint violations.
    
    Parameters:
    -----------
    table : sqlalchemy.Table
        The SQLAlchemy table object where the row will be inserted.
    data : dict
        A dictionary containing column names and their corresponding values for the row to insert.
    retries : int, optional (default=5)
        Number of retry attempts in case of a unique constraint violation.
    delay : int, optional (default=1)
        Delay in seconds between retries.

    Raises:
    -------
    SQLAlchemyError
        If an error other than a unique constraint violation occurs.

    Example:
    --------
    insert_row(table=CustomerTable, data={"id": 1, "name": "John Doe"})
    """
    session = Session()
    try:
        # Attempt to insert the row
        print(f"Inserting data: {data}")
        session.execute(table.insert().values(**data))
        session.commit()
        print("Row inserted successfully.")
    except SQLAlchemyError as e:
        # Handle unique constraint violation and retry if needed
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            print(f"Primary key conflict: {e}. Retrying...")
            if retries > 0:
                time.sleep(delay)  # Wait before retrying
                return insert_row(table, data, retries-1, delay)
            else:
                print("Max retries reached. Could not insert row.")
        else:
            print(f"Error inserting row: {e}")
            session.rollback()
    finally:
        session.close()


def delete_row(table, conditions):
    """
    Deletes rows from a specified table based on given conditions.

    Parameters:
    -----------
    table : sqlalchemy.Table
        The SQLAlchemy table object from which rows will be deleted.
    conditions : dict
        A dictionary where keys are column names and values are the matching values to filter rows.

    Raises:
    -------
    SQLAlchemyError
        If an error occurs during the deletion.

    Example:
    --------
    delete_row(table=CustomerTable, conditions={"id": 1, "name": "John Doe"})
    """
    session = Session()
    try:
        query = table.delete().where(
            *[table.c[key] == value for key, value in conditions.items()]
        )
        session.execute(query)
        session.commit()
        print("Row(s) deleted successfully.")
    except SQLAlchemyError as e:
        print(f"Error deleting row(s): {e}")
        session.rollback()
    finally:
        session.close()

def export_to_dataframe(table):
    """
    Exports all rows from a specified table into a Pandas DataFrame.

    Parameters:
    -----------
    table : sqlalchemy.Table
        The SQLAlchemy table object to export data from.

    Returns:
    --------
    pd.DataFrame
        A Pandas DataFrame containing all rows from the specified table.

    Raises:
    -------
    SQLAlchemyError
        If an error occurs during the data export.

    Example:
    --------
    df = export_to_dataframe(table=CustomerTable)
    """
    session = Session()
    try:
        query = session.query(table)
        df = pd.read_sql(query.statement, session.bind)
        return df
    except SQLAlchemyError as e:
        print(f"Error exporting to DataFrame: {e}")
    finally:
        session.close()
