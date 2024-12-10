"""
Data Generation Script

This script uses the Faker library and predefined datasets to generate mock data for movies, customers, subscriptions, segments, engagements, and A/B tests (the rest of the tables are filled after running the models).
Each data generator ensures consistency with predefined values or creates random but realistic mock data for testing and development.

Modules:
    - Faker: Generates somewhat realistic random data for names, emails, dates, etc.
    - pandas: Data manipulation library (not yet used in this script but imported just because).
    - random: Used for generating random values like session durations or probabilities.
    - logging: Standard Python logging library (not used yet in the script, same reason as pandas).
    - loguru: Logging library for better formatting (imported but unused in this script, you get it).
"""

from faker import Faker
import pandas as pd
import random
import logging

import os
from loguru import logger
fake=Faker()

random.seed(10)

# -----------------------------------------------------
# Predefined Dataset for Movies (real ones)
# -----------------------------------------------------

real_films = [
    {"movie_id": 1, "movie_name": "Inception", "release_year": 2010, "movie_rating": 8.8, "movie_genre": "Sci-Fi", "movie_duration": 148},
    {"movie_id": 2, "movie_name": "The Godfather", "release_year": 1972, "movie_rating": 9.2, "movie_genre": "Crime", "movie_duration": 175},
    {"movie_id": 3, "movie_name": "The Dark Knight", "release_year": 2008, "movie_rating": 9.0, "movie_genre": "Action", "movie_duration": 152},
    {"movie_id": 4, "movie_name": "Pulp Fiction", "release_year": 1994, "movie_rating": 8.9, "movie_genre": "Drama", "movie_duration": 154},
    {"movie_id": 5, "movie_name": "Forrest Gump", "release_year": 1994, "movie_rating": 8.8, "movie_genre": "Comedy", "movie_duration": 142},
    {"movie_id": 6, "movie_name": "The Matrix", "release_year": 1999, "movie_rating": 8.7, "movie_genre": "Sci-Fi", "movie_duration": 136},
    {"movie_id": 7, "movie_name": "Fight Club", "release_year": 1999, "movie_rating": 8.8, "movie_genre": "Drama", "movie_duration": 139},
    {"movie_id": 8, "movie_name": "Interstellar", "release_year": 2014, "movie_rating": 8.6, "movie_genre": "Sci-Fi", "movie_duration": 169},
    {"movie_id": 9, "movie_name": "The Lord of the Rings: The Return of the King", "release_year": 2003, "movie_rating": 8.9, "movie_genre": "Fantasy", "movie_duration": 201},
    {"movie_id": 10, "movie_name": "The Shawshank Redemption", "release_year": 1994, "movie_rating": 9.3, "movie_genre": "Drama", "movie_duration": 142},
]

# -----------------------------------------------------
# Data Generator Functions
# -----------------------------------------------------

def generate_movie(movie_id):
    """
    Retrieve a predefined movie from the list based on its ID.

    Args:
        movie_id (int): The ID of the movie to retrieve.

    Returns:
        dict: A dictionary containing movie details.

    Raises:
        ValueError: If the movie_id is invalid.
    """
    if 1 <= movie_id <= len(real_films):
        return real_films[movie_id - 1]
    else:
        raise ValueError("Invalid movie_id: no predefined product exists with this ID.")

def generate_subscription(subscription_id):
    """
    Retrieve a predefined subscription plan based on its ID.

    Args:
        subscription_id (int): The ID of the subscription to retrieve.

    Returns:
        dict: A dictionary containing subscription details.

    Raises:
        ValueError: If the subscription_id is invalid.
    """
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

def generate_segment(segment_id):
    """
    Retrieve a predefined customer segment based on its ID.

    Args:
        segment_id (int): The ID of the segment to retrieve.

    Returns:
        dict: A dictionary containing segment details.

    Raises:
        ValueError: If the segment_id is invalid.
    """
    predefined_segments = [
        {"segment_id": 1, 
         "segment_name": "Lost Cause",
         "segment_description": "Customers with minimal engagement and low value."},
        {"segment_id": 2, 
         "segment_name": "Vulnerable Customers", 
         "segment_description": "At-risk customers who can be retained."},
        {"segment_id": 3, 
         "segment_name": "Free Riders", 
         "segment_description": "Customers who use free services with low revenue contribution."},
        {"segment_id": 4, 
         "segment_name": "Star Customers", 
         "segment_description": "High-value customers who are highly engaged and loyal."},
    ]

    if 1 <= segment_id <= len(predefined_segments):
        return predefined_segments[segment_id - 1]
    else:
        raise ValueError("Invalid subscription_id: no predefined subscription exists with this ID.")
    
def generate_customer(subscription_id):
    """
    Generate a mock customer record.

    Args:
        customer_id (int): The unique ID of the customer.
        subscription_id (int): The subscription ID associated with the customer.

    Returns:
        dict: A dictionary containing customer details.
    """
    created_at = fake.date_time_this_decade()
    updated_at = fake.date_time_between(start_date=created_at, end_date="now")
    return {
        "name": fake.name(),
        "email": fake.email(),
        "subscription_id": subscription_id,
        "location": fake.city(),
        "created_at": created_at,
        "updated_at": updated_at,
    }

def generate_engagement(engagement_id, customer_id, movie_id):
    """
    Generate a mock engagement record between a customer and a movie.

    Args:
        engagement_id (int): The unique ID of the engagement.
        customer_id (int): The customer involved in the engagement.
        movie_id (int): The movie involved in the engagement.

    Returns:
        dict: A dictionary containing engagement details.
    """
    return {
        "engagement_id": engagement_id,
        "customer_id": customer_id,
        "movie_id": movie_id,
        "session_date": fake.date_this_year(),
        "session_duration": random.randint(1, 360),
        "watched_fully": fake.boolean(chance_of_getting_true=60),
        "like_status": fake.random_element(elements=["Liked", "Disliked", "No Action"]),
    }


def generate_ab_test(ab_test_id):
    """
    Retrieve a predefined A/B test configuration based on its ID.

    Args:
        ab_test_id (int): The ID of the A/B test to retrieve.

    Returns:
        dict: A dictionary containing A/B test details.

    Raises:
        ValueError: If the ab_test_id is invalid.
    """
    predefined_types = [
        {
            "ab_test_id": 1,
            "goal": "subscription",
            "targeting": "subscription_plan",
            "test_variant": 1,
            "text_skeleton": "Simple. Affordable. Amazing. The (insert your subscription plan here) plan is yours today for just (insert your price here). What are you waiting for?" 
        },
        {
            "ab_test_id": 2,
            "goal": "subscription",
            "targeting": "subscription_plan",
            "test_variant": 2,
            "text_skeleton": "You deserve the best, and the (insert your subscription plan here) plan gives you just that—for only (insert your price here). Start your premium experience today!"
        },
        {
            "ab_test_id": 3,
            "goal": "engagement",
            "targeting": "by movie",
            "test_variant": 1,
            "text_skeleton": "Looking for your next favorite movie? (insert the movie here) is a must-watch. Start streaming today!"
        },
        {
            "ab_test_id": 4,
            "goal": "engagement",
            "targeting": "by movie",
            "test_variant": 2,
            "text_skeleton": "Make tonight special with (insert the movie here). The perfect pick for your next binge session!"
        },
        {
            "ab_test_id": 5,
            "goal": "engagement",
            "targeting": "by genre",
            "test_variant": 1,
            "text_skeleton": "Can't get enough of (insert your genre)? We've got you covered! Start streaming the best titles now."
        },{
            "ab_test_id": 6,
            "goal": "engagement",
            "targeting": "by genre",
            "test_variant": 2,
            "text_skeleton": "Join millions of fans enjoying the best of (insert your genre). Don't wait—start streaming now!"
        },
    ]

    if 1 <= ab_test_id <= len(predefined_types):
        return predefined_types[ab_test_id - 1]
    else:
        raise ValueError("Invalid segment_id: no predefined segment exists with this ID.")


