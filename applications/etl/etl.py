"""
ETL Script for Generating and Loading Data into our Streaming Platform Database.

This script generates data for subscriptions, customers, movies, engagements, A/B tests, segments, and related entities.
It saves the generated data into CSV files and loads the CSV data into the respective database tables. The data can be viewed manually using PGAdmin.

Modules:
    - models: Database models for the project.
    - database: Database engine and base class.
    - data_generator: Functions to generate mock (and real) data for the various entities.
    - pandas: For data manipulation and storage in CSV format.
    - loguru: For structured logging.
    - random: For random number generation.
    - sqlalchemy.orm: For managing database sessions.
    - glob, os: For file and system operations.
    - time: For delays in the script execution.
"""

from models import *
from database import engine, Base
import time
import pandas as pd
from loguru import logger
import random
from sqlalchemy.orm import sessionmaker
from data_generator import (
    generate_movie,
    generate_customer,
    generate_engagement,
    generate_ab_test,
    generate_subscription,
    generate_segment
)


# -----------------------------------------------------
# Pause Script Execution
# -----------------------------------------------------
print("Pausing for 60 seconds...")
time.sleep(60)
print("Resuming execution.")

# -----------------------------------------------------
# Seed for Random Number Generator (to replicate the results)
# -----------------------------------------------------
random.seed(10)

# -----------------------------------------------------
# Constants (for generating a specific number of rows)
# -----------------------------------------------------
NUMBER_OF_CUSTOMERS = 2000
NUMBER_OF_ENGAGEMENTS = 10000
NUMBER_OF_AB_TESTS = 6
NUMBER_OF_SUBSCRIPTIONS = 4
NUMBER_OF_MOVIES = 10
NUMBER_OF_SEGMENTS = 4

# -----------------------------------------------------
# Generate and Save Data to CSV Files
# -----------------------------------------------------

# Generate Subscriptions
subscriptions = pd.DataFrame(
    [generate_subscription(subscription_id) for subscription_id in range(1, NUMBER_OF_SUBSCRIPTIONS + 1)]
)
logger.info('Subscription Data')
logger.info(subscriptions.head())
subscriptions.to_csv('data/subscriptions.csv', index=False)
logger.info(f'Subscription Data saved to CSV: {subscriptions.shape}')

# Generate Customers
customers = pd.DataFrame(
    [generate_customer(random.randint(1, NUMBER_OF_SUBSCRIPTIONS)) for _ in range(1, NUMBER_OF_CUSTOMERS + 1)]
)
logger.info('Customer Data')
logger.info(customers.head())
customers.to_csv('data/customers.csv', index=False)
logger.info(f'Customer Data saved to CSV: {customers.shape}')

# Generate AB Tests
ab_tests = pd.DataFrame(
    [generate_ab_test(ab_test_id) for ab_test_id in range(1, NUMBER_OF_AB_TESTS + 1)]
)
logger.info('AB Test Data')
logger.info(ab_tests.head())
ab_tests.to_csv('data/ab_tests.csv', index=False)
logger.info(f'AB Test Data saved to CSV: {ab_tests.shape}')

# Generate Movies
movies = pd.DataFrame(
    [generate_movie(movie_id) for movie_id in range(1, NUMBER_OF_MOVIES + 1)]
)
logger.info('Movie Data')
logger.info(movies.head())
movies.to_csv('data/movies.csv', index=False)
logger.info(f'Movie Data saved to CSV: {movies.shape}')

# Generate Engagements
engagements = pd.DataFrame(
    [generate_engagement(engagement_id, customer_id=random.randint(1, NUMBER_OF_CUSTOMERS), movie_id=random.randint(1, NUMBER_OF_MOVIES))
     for engagement_id in range(1, NUMBER_OF_ENGAGEMENTS + 1)]
)
logger.info('Engagement Data')
logger.info(engagements.head())
engagements.to_csv('data/engagements.csv', index=False)
logger.info(f'Engagement Data saved to CSV: {engagements.shape}')

# Generate Segments
segments = pd.DataFrame(
    [generate_segment(segment_id) for segment_id in range(1, NUMBER_OF_SEGMENTS + 1)]
)
logger.info('Segment Data')
logger.info(segments.head())
segments.to_csv('data/segments.csv', index=False)
logger.info(f'Segment Data saved to CSV: {segments.shape}')

# Empty Table for Customer Segments
customer_segments = pd.DataFrame(columns=["customer_segment_id", "customer_id", "segment_id"])
logger.info('Customer Segment Data (Empty)')
logger.info(customer_segments)
customer_segments.to_csv('data/customer_segments.csv', index=False)
logger.info('Customer Segment Data saved to CSV.')

# Empty Table for AB Test Results
ab_test_results = pd.DataFrame(columns=["result_id", "ab_test_id", "customer_id", "experiment_id", "clicked_link"])
logger.info('AB Test Results Data (Empty)')
logger.info(ab_test_results)
ab_test_results.to_csv('data/ab_test_results.csv', index=False)
logger.info('AB Test Results Data saved to CSV.')

# Empty Table for Experiments
experiments = pd.DataFrame(columns=["experiment_id", "p_value"])
logger.info('Experiments Data (Empty)')
logger.info(experiments)
experiments.to_csv('data/experiments.csv', index=False)
logger.info('Experiments Data saved to CSV.')

# -----------------------------------------------------
# Load CSV Data into Database Tables
# -----------------------------------------------------

def load_csv_to_table(table_name, csv_path):
    """
    Load data from a CSV file into a database table.

    **Parameters:**
    
    - `table_name (str):` The name of the database table.
    - `csv_path (str):` The path to the CSV file containing data.

    **Returns:**
        - `None`
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f'Loading {table_name}')

# Load data from CSVs into the database
import glob
from os import path

folder_path = "data/*.csv"

files = glob.glob(folder_path)
base_names = [path.splitext(path.basename(file))[0] for file in files]
for table in base_names:
    try:
        load_csv_to_table(table, path.join("data/", f"{table}.csv"))
    except Exception as e:
        print(f"Failed to ingest table {table}. Moving to the next!")

print("Tables are populated.")

