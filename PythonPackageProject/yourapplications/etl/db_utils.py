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
    Inserts a row into the specified table and handles unique constraint errors.
    :param table: SQLAlchemy table object
    :param data: Dictionary containing column names and values
    :param retries: Number of retry attempts
    :param delay: Delay (in seconds) between retries
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
    Deletes rows from a specified table based on conditions.
    :param table: SQLAlchemy table object
    :param conditions: Dictionary of column-value pairs for the WHERE clause
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
    :param table: SQLAlchemy table object
    :return: Pandas DataFrame
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
