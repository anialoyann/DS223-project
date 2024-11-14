from faker import Faker
import pandas as pd
import random
import logging

import os
from loguru import logger
fake=Faker()

real_films = [
    {"product_id": 1, "name": "Inception", "release_year": 2010, "rating": 8.8},
    {"product_id": 2, "name": "The Godfather", "release_year": 1972, "rating": 9.2},
    {"product_id": 3, "name": "The Dark Knight", "release_year": 2008, "rating": 9.0},
    {"product_id": 4, "name": "Pulp Fiction", "release_year": 1994, "rating": 8.9},
    {"product_id": 5, "name": "Forrest Gump", "release_year": 1994, "rating": 8.8},
    {"product_id": 6, "name": "The Matrix", "release_year": 1999, "rating": 8.7},
    {"product_id": 7, "name": "Fight Club", "release_year": 1999, "rating": 8.8},
    {"product_id": 8, "name": "Interstellar", "release_year": 2014, "rating": 8.6},
    {"product_id": 9, "name": "The Lord of the Rings: The Return of the King", "release_year": 2003, "rating": 8.9},
    {"product_id": 10, "name": "The Shawshank Redemption", "release_year": 1994, "rating": 9.3},
]
def generate_product(product_id):
    if 1 <= product_id <= len(real_films):
        return real_films[product_id - 1]
    else:
        raise ValueError("Invalid product_id: no predefined product exists with this ID.")

def generate_subscription(subscription_id):
    predefined_subscriptions = [
        {"subscription_id": 1, "subscription_name": "Student", "price": 5},
        {"subscription_id": 2, "subscription_name": "Family", "price": 10},
        {"subscription_id": 3, "subscription_name": "Basic", "price": 7},
        {"subscription_id": 4, "subscription_name": "Premium", "price": 9},
    ]

    if 1 <= subscription_id <= len(predefined_subscriptions):
        return predefined_subscriptions[subscription_id - 1]
    else:
        raise ValueError("Invalid subscription_id: no predefined subscription exists with this ID.")


def generate_customer(customer_id, subscription_id):
    created_at = fake.date_time_this_decade()
    updated_at = fake.date_time_between(start_date=created_at, end_date="now")
    return {
        "customer_id": customer_id,
        "name": fake.name(),
        "email": fake.email(),
        "subscription_id": subscription_id,
        "location": fake.city(),
        "created_at": created_at,
        "updated_at": updated_at,
    }

def generate_engagement(engagement_id, customer_id, product_id):
    return {
        "engagement_id": engagement_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "session_duration": random.randint(1, 360),
        "session_date": fake.date_this_year(),
        "device_type": fake.random_element(elements=["Mobile", "Desktop", "Tablet"]),
        "watched_fully": fake.boolean(chance_of_getting_true=60)
    }


def generate_ab_test(ab_test_id):
    predefined_types = [
        {
            "ab_test_id": 1,
            "test_variant": 1,
            "test_goal": "Streaming"
        },
        {
            "ab_test_id": 2,
            "test_variant": 2,
            "test_goal": "Streaming"
        },
        {
            "ab_test_id": 3,
            "test_variant": 1,
            "test_goal": "Subscription"
        },
        {
            "ab_test_id": 4,
            "test_variant": 2,
            "test_goal": "Subscription"
        },
    ]

    if 1 <= ab_test_id <= len(predefined_types):
        return predefined_types[ab_test_id - 1]
    else:
        raise ValueError("Invalid segment_id: no predefined segment exists with this ID.")


