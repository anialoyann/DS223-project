from models import *
from database import engine, Base
import time

 # Pause code execution for 10 seconds
print("Pausing for 20 seconds...")
time.sleep(60)
print("Resuming execution.")

from data_generator import (
    generate_product,
    generate_customer,
    generate_engagement,
    generate_ab_test,
    generate_subscription
)

import pandas as pd
from loguru import logger
import random

NUMBER_OF_CUSTOMERS=2000
NUMBER_OF_ENGAGEMENTS = 10000 
NUMBER_OF_AB_TESTS = 4
NUMBER_OF_SUBSCRIPTIONS = 4
NUMBER_OF_PRODUCTS = 10


subscriptions = pd.DataFrame(
    [generate_subscription(subscription_id) for subscription_id in range(1, NUMBER_OF_SUBSCRIPTIONS + 1)]
)
logger.info('Subscription Data')
logger.info(subscriptions.head())
subscriptions.to_csv('data/subscriptions.csv', index=False)
logger.info(f'Subscription Data saved to csv: {subscriptions.shape}')

customers = pd.DataFrame(
    [generate_customer(customer_id, random.randint(1, NUMBER_OF_SUBSCRIPTIONS)) for customer_id in range(1, NUMBER_OF_CUSTOMERS + 1)]
)
logger.info('Customer Data')
logger.info(customers.head())
customers.to_csv('data/customers.csv', index=False)
logger.info(f'Customer Data saved to csv: {customers.shape}')

ab_tests = pd.DataFrame(
    [generate_ab_test(ab_test_id) for ab_test_id in range(1, NUMBER_OF_AB_TESTS + 1)]
)
logger.info('AB Test Data')
logger.info(ab_tests.head())
ab_tests.to_csv('data/ab_tests.csv', index=False)
logger.info(f'AB Test Data saved to csv: {ab_tests.shape}')

products = pd.DataFrame(
    [generate_product(product_id) for product_id in range(1, NUMBER_OF_PRODUCTS + 1)]
)
logger.info('Product Data')
logger.info(products.head())
products.to_csv('data/products.csv', index=False)
logger.info(f'Product Data saved to csv: {products.shape}')

engagements = pd.DataFrame(
    [generate_engagement(engagement_id, customer_id=random.randint(1, NUMBER_OF_CUSTOMERS), product_id=random.randint(1, NUMBER_OF_PRODUCTS))
     for engagement_id in range(1, NUMBER_OF_ENGAGEMENTS + 1)]
)
logger.info('Engagement Data')
logger.info(engagements.head())
engagements.to_csv('data/engagements.csv', index=False)
logger.info(f'Engagement Data saved to csv: {engagements.shape}')

def load_csv_to_table(table_name, csv_path):
    """
    Load data from a CSV file into a database table.

    Args:
    - table_name: Name of the database table.
    - csv_path: Path to the CSV file containing data.

    Returns:
    - None
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f'loading {table_name}')


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

