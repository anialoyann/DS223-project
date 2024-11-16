# Successfully tested by data scientist

from sqlalchemy import MetaData, Table
from db_utils import insert_row, export_to_dataframe
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".env")

# Validate that DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables.")

# Import the engine from db_utils.py after the .env is loaded
from db_utils import engine

# Load metadata and reflect the movies table
metadata = MetaData()
metadata.reflect(bind=engine)
movies_table = metadata.tables.get("movies")

# Data to insert - FILL THIS IN BEFORE RUNNING AND MAKE SURE YOU'RE RUNNING FROM INSIDE THE CONTAINER ETL
movie_data = {
    "movie_name": "Hunger Games : The Ballad of Songbirds and Snakes",
    "release_year": 2023 ,
    "movie_duration": 157,
    "movie_rating": 10000000000000000000000000000 ,
    "movie_genre": "dystopian"
    }

def main():
    # Insert a new movie
    print("Inserting movie data...")
    insert_row(movies_table, movie_data)
    
    # Export the movies table to a DataFrame and display it
    print("Exporting movies table to DataFrame...")
    df = export_to_dataframe(movies_table)
    print(df)

if __name__ == "__main__":
    main()