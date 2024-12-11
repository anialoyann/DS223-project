from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database1 import Base
from datetime import datetime, timezone



# Segments Model
class Segment(Base):
    """
    Represents a customer segment.

    **Attributes:**
    - `segment_id (int)`: Primary key, unique identifier for each segment.
    - `segment_name (str)`: Name of the customer segment.
    - `segment_description (str)`: Detailed description of the segment.
    - `customers (relationship)`: Association with the `CustomerSegment` model for linked customers.
    """
    __tablename__ = "segments"
    segment_id = Column(Integer, primary_key=True, index=True)
    segment_name = Column(String, nullable=False)
    segment_description = Column(Text)
    customers = relationship("CustomerSegment", back_populates="segment")

# Customers Model
class Customer(Base):
    """
    Represents a customer in the system.

    **Attributes:**
    - `customer_id (int)`: Primary key, unique identifier for each customer.
    - `name (str)`: Customer's name.
    - `email (str)`: Unique email address of the customer.
    - `subscription_id (int)`: Foreign key linking to the `Subscription` model.
    - `location (str)`: Geographic location of the customer.
    - `created_at (DateTime)`: Timestamp of when the customer was added.
    - `updated_at (DateTime)`: Timestamp of the last update.
    - `segments (relationship)`: Association with the `CustomerSegment` model.
    - `engagements (relationship)`: Association with the `Engagement` model for movie interactions.
    - `ab_test_results (relationship)`: Association with the `ABTestResult` model for test results.
    """
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id"))
    location = Column(String)
    created_at = Column(DateTime, default=datetime.now())  
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    segments = relationship("CustomerSegment", back_populates="customer")
    engagements = relationship("Engagement", back_populates="customer")
    ab_test_results = relationship("ABTestResult", back_populates="customer")

# Customer Segments Model
class CustomerSegment(Base):
    """
    Represents the relationship between customers and segments.

    **Attributes:**
    - `customer_segment_id (int)`: Primary key for this association.
    - `customer_id (int)`: Foreign key linking to the `Customer` model.
    - `segment_id (int)`: Foreign key linking to the `Segment` model.
    - `customer (relationship)`: Association with the `Customer` model.
    - `segment (relationship)`: Association with the `Segment` model.
    """
    __tablename__ = "customer_segments"
    customer_segment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))
    customer = relationship("Customer", back_populates="segments")
    segment = relationship("Segment", back_populates="customers")

# Movies Model
class Movie(Base):
    """
    Represents a movie in the system.

    **Attributes:**
    - `movie_id (int)`: Primary key, unique identifier for each movie.
    - `movie_name (str)`: Name of the movie.
    - `movie_rating (float)`: Rating of the movie, typically out of 10.
    - `movie_duration (int)`: Duration of the movie in minutes.
    - `movie_genre (str)`: Genre or category of the movie.
    - `release_year (int)`: Year the movie was released.
    """
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True, index=True)
    movie_name = Column(String, nullable=False)
    movie_rating = Column(Float)
    movie_duration = Column(Integer)
    movie_genre = Column(String)
    release_year = Column(Integer)

# Engagements Model
class Engagement(Base):
    """
    Represents a customer's interaction with a movie.

    **Attributes:**
    - `engagement_id (int)`: Primary key for this engagement record.
    - `customer_id (int)`: Foreign key linking to the `Customer` model.
    - `movie_id (int)`: Foreign key linking to the `Movie` model.
    - `watched_fully (bool)`: Indicates if the movie was watched completely.
    - `like_status (str)`: Feedback status ('like', 'dislike', or 'neutral').
    - `date_watched (DateTime)`: Timestamp of when the movie was watched.
    - `customer (relationship)`: Association with the `Customer` model.
    - `movie (relationship)`: Association with the `Movie` model.
    """
    __tablename__ = "engagements"
    engagement_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    watched_fully = Column(Boolean)
    like_status = Column(String)
    date_watched = Column(DateTime)
    customer = relationship("Customer", back_populates="engagements")
    movie = relationship("Movie")

# Subscriptions Model
class Subscription(Base):
    """
    Represents a subscription plan available to customers.

    **Attributes:**
    - `subscription_id (int)`: Primary key, unique identifier for each subscription.
    - `subscription_name (str)`: Name of the subscription plan.
    - `price (int)`: Cost of the subscription plan in the given currency.
    """
    __tablename__ = "subscriptions"
    subscription_id = Column(Integer, primary_key=True, index=True)
    subscription_name = Column(String, nullable=False)
    price = Column(Integer)

# AB Tests Model
class ABTest(Base):
    """
    Represents an A/B testing experiment.

    **Attributes:**
    - `ab_test_id (int)`: Primary key for the A/B test.
    - `goal (str)`: Objective of the test ('Engagement' or 'Subscription').
    - `targeting (str)`: Focus of the test ('genre', 'movie', or 'package').
    - `test_variant (int)`: Identifier for the test variant (A or B).
    - `text_skeleton (str)`: Template text used in the test.
    - `results (relationship)`: Association with the `ABTestResult` model.
    """
    __tablename__ = "ab_tests"
    ab_test_id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, nullable=False)  # 'Engagement' or 'Subscription'
    targeting = Column(String, nullable=False)  # 'genre', 'movie', or 'package'
    test_variant = Column(Integer)  # A/B Test variant identifier
    text_skeleton = Column(Text)  # Text template used in the A/B Test
    results = relationship("ABTestResult", back_populates="ab_test")

# AB Test Results Model
class ABTestResult(Base):
    """
    Represents the results of an A/B test for a specific customer.

    **Attributes:**
    - `result_id (int)`: Primary key for this result.
    - `ab_test_id (int)`: Foreign key linking to the `ABTest` model.
    - `experiment_id (int)`: Foreign key linking to the `Experiment` model.
    - `customer_id (int)`: Foreign key linking to the `Customer` model.
    - `clicked_link (bool)`: Indicates if the customer clicked the test link.
    - `ab_test (relationship)`: Association with the `ABTest` model.
    - `customer (relationship)`: Association with the `Customer` model.
    - `experiment (relationship)`: Association with the `Experiment` model.
    """
    __tablename__ = "ab_test_results"
    result_id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    ab_test_id = Column(Integer, ForeignKey("ab_tests.ab_test_id"))
    experiment_id = Column(Integer, ForeignKey("experiments.experiment_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    clicked_link = Column(Boolean)
    ab_test = relationship("ABTest", back_populates="results")
    customer = relationship("Customer", back_populates="ab_test_results")
    experiment = relationship("Experiment", back_populates="ab_test_results")

# Experiments Model (New Table)
class Experiment(Base):
    """
    Represents an experimental setup used for A/B testing.

    **Attributes:**
    - `experiment_id (int)`: Primary key for the experiment.
    - `p_value (float)`: Statistical significance value for the experiment.
    - `ab_test_results (relationship)`: Association with the `ABTestResult` model.
    """
    __tablename__ = "experiments"
    experiment_id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    p_value = Column(Float)
    ab_test_results = relationship("ABTestResult", back_populates="experiment")
