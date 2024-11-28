"""
Database Models for the Analytics Platform.

This module defines database models using SQLAlchemy for subscriptions, movies, customers, 
segments, engagements, A/B tests, experiments, and their results.

Modules:
    - sqlalchemy: For ORM and database schema definition.
    - datetime: For handling timestamp fields.
    - loguru: For logging events.
    - database: Includes the Base and engine configuration for SQLAlchemy.

Classes:
    - `Subscription`: Represents different subscription plans.
    - `Movie`: Represents movies with details like release year, genre and rating.
    - `Customer`: Represents customer data, including subscription plans.
    - `Segment`: Represents customer segments for analytics.
    - `CustomerSegment`: Represents the customers and the segments they are sorted into.
    - `Engagement`: Represents customer engagement with movies.
    - `ABTest`: Represents descriptions of our A/B tests.
    - `Experiment`: Represents experiments related to A/B tests.
    - `ABTest_Result`: Represents results and metrics of A/B tests.
"""


from loguru import logger


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from database import Base, engine

Base= declarative_base()

class Subscription(Base):
    """
    Represents subscription plans for the platform.

    **Attributes:**
    - `subscription_id (int):` Unique identifier for the subscription.
    - `subscription_name (str):` Name of the subscription plan.
    - `price (int):` Price of the subscription plan.
    """
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True)
    subscription_name = Column(String)
    price = Column(Integer)

class Movie(Base):
    """
    Represents a movie available on the platform.

    **Attributes:**
    - `movie_id (int):` Unique identifier for the movie.
    - `movie_name (str):` Name of the movie.
    - `release_year (int):` Release year of the movie.
    - `movie_duration (int):` Duration of the movie in minutes.
    - `movie_rating (float):` Average rating of the movie.
    - `movie_genre (str):` Genre of the movie.
    """
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String)
    release_year = Column(Integer)
    movie_duration = Column(Integer)
    movie_rating = Column(Float)
    movie_genre = Column(String)

class Customer(Base):
    """
    Represents a customer using the platform.

    **Attributes:**
    - `customer_id (int):` Unique identifier for the customer.
    - `name (str):` Name of the customer.
    - `email (str):` Email address of the customer.
    - `subscription_id (int):` ID of the customer's subscription plan.
    - `location (str):` Location (city) of the customer.
    - `created_at (datetime):` Account creation timestamp.
    - `updated_at (datetime):` Last update timestamp.
    - `subscription (Subscription):` Relationship to the Subscription model.
    """
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id"))
    location = Column(String)
    created_at = Column(DateTime) 
    updated_at = Column(DateTime)

    subscription = relationship("Subscription")

class Segment(Base):
    """
    Represents a customer segment for analysis or targeting.

    **Attributes:**
    - `segment_id (int):` Unique identifier for the segment.
    - `segment_name (str):` Name of the segment.
    - `segment_description (str):` Description of the segment.
    """
    __tablename__ = "segments"

    segment_id = Column(Integer, primary_key=True)
    segment_name = Column(String)
    segment_description = Column(Text)

class CustomerSegment(Base):
    """
    Represents the mapping between customers and segments.

    **Attributes:**
    - `customer_segment_id (int):` Unique identifier for the mapping.
    - `customer_id (int):` ID of the associated customer.
    - `segment_id (int):` ID of the associated segment.
    - `customer (Customer):` Relationship to the Customer model.
    - `segment (Segment):` Relationship to the Segment model.
    """
    __tablename__ = "customer_segments"

    customer_segment_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))

    customer = relationship("Customer")
    segment = relationship("Segment")

class Engagement(Base):
    """
    Represents customer engagement with movies.

    **Attributes:**
    - `engagement_id (int):` Unique identifier for the engagement.
    - `customer_id (int):` ID of the associated customer.
    - `movie_id (int):` ID of the associated movie.
    - `session_date (datetime):` Timestamp of the engagement session.
    - `session_duration (int):` Duration of the session in minutes.
    - `watched_fully (bool):` Whether the movie was watched completely.
    - `like_status (str):` Like/dislike status of the movie.
    - `customer (Customer):` Relationship to the Customer model.
    - `movie (Movie):` Relationship to the Movie model.
    """
    __tablename__ = "engagements"
    
    engagement_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    movie_id =  Column(Integer, ForeignKey("movies.movie_id"))
    session_date = Column(DateTime)
    session_duration = Column(Integer)
    watched_fully = Column(Boolean)
    like_status = Column(String)

    customer = relationship("Customer")
    movie = relationship("Movie")

class ABTest(Base):
    """
    Represents metadata for an A/B test.

    **Attributes:**
    - `ab_test_id (int):` Unique identifier for the A/B test.
    - `goal (str):` Goal of the test.
    - `targeting (str):` Targeting criteria for the test.
    - `test_variant (int):` Variant number of the test.
    - `text_skeleton (str):` A text skeleton for conducting the test.
    """
    __tablename__ = "ab_tests"
    
    ab_test_id = Column(Integer, primary_key=True)
    goal = Column(String)
    targeting = Column(String)
    test_variant = Column(Integer)
    text_skeleton = Column(Text)

class Experiment(Base):
    """
    Represents an experiment tied to A/B tests.

    **Attributes:**
    - `experiment_id (int):` Unique identifier for the experiment.
    - `p_value (float):` Statistical p-value for the experiment.
    """
    __tablename__ = "experiments"
    
    experiment_id = Column(Integer, primary_key=True)
    p_value = Column(Float)

class ABTest_Result(Base):
    """
    Represents results from A/B tests.

    **Attributes:**
    - `result_id (int):` Unique identifier for the result.
    - `ab_test_id (int):` ID of the associated A/B test.
    - `customer_id (int):` ID of the associated customer.
    - `experiment_id (int):` ID of the associated experiment.
    - `clicked_link (bool):` Whether the customer clicked the link.
    - `customer (Customer):` Relationship to the Customer model.
    - `abtest (ABTest):` Relationship to the ABTest model.
    - `experiment (Experiment):` Relationship to the Experiment model.
    """
    __tablename__ = "ab_test_results"

    result_id = Column(Integer, primary_key=True)
    ab_test_id = Column(Integer, ForeignKey("ab_tests.ab_test_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    experiment_id = Column(Integer, ForeignKey("experiments.experiment_id"))
    clicked_link = Column(Boolean)

    customer = relationship("Customer")
    abtest = relationship("ABTest")
    experiment = relationship('Experiment')
    
Base.metadata.create_all(engine)

