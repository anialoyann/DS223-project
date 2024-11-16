from faker import Faker
import pandas as pd
import random
import logging

import os
from loguru import logger
fake=Faker()

random.seed(10)

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

def generate_movie(movie_id):
    if 1 <= movie_id <= len(real_films):
        return real_films[movie_id - 1]
    else:
        raise ValueError("Invalid movie_id: no predefined product exists with this ID.")

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

def generate_segment(segment_id):
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

def generate_engagement(engagement_id, customer_id, movie_id):
    return {
        "engagement_id": engagement_id,
        "customer_id": customer_id,
        "movie_id": movie_id,
        "session_duration": random.randint(1, 360),
        "session_date": fake.date_this_year(),
        "device_type": fake.random_element(elements=["Mobile", "Desktop", "Tablet"]),
        "watched_fully": fake.boolean(chance_of_getting_true=60),
        "like_status": fake.random_element(elements=["Liked", "Disliked", "No Action"]),
    }


def generate_ab_test(ab_test_id):
    predefined_types = [
        {
            "ab_test_id": 1,
            "goal": "subscription",
            "targeting": "by genre",
            "test_variant": 1,
            "text_skeleton": "Unlock exclusive access to top-rated (insert_genre) movies! Subscribe now for just (insert_price) ."
        },
        {
            "ab_test_id": 2,
            "goal": "subscription",
            "targeting": "subscription sale",
            "test_variant": 2,
            "text_skeleton": "Special deal for (insert_subscription_name) subscribers: Only (insert price) for a limited time!"
        },
        {
            "ab_test_id": 3,
            "goal": "engagement",
            "targeting": "by movie",
            "test_variant": 1,
            "text_skeleton": "Have you seen (insert_movies)? Don't missout! Watch now and enjoy the experience."
        },
        {
            "ab_test_id": 4,
            "goal": "engagement",
            "targeting": "by genre",
            "test_variant": 2,
            "text_skeleton": "Experience the magic of (insert_genre) likenever before. Click here and start watching!"
        }
    ]

    if 1 <= ab_test_id <= len(predefined_types):
        return predefined_types[ab_test_id - 1]
    else:
        raise ValueError("Invalid segment_id: no predefined segment exists with this ID.")


