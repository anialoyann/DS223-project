from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone

# Base Schema for common fields
class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.

    **Config:**
    - `orm_mode`: Enables compatibility with SQLAlchemy models for easy conversion.
    """
    class Config:
        orm_mode = True

class SegmentCreate(BaseModel):
    """
    Schema for creating a new Segment.
    """
    pass

class Segment(BaseModel):
    """
    Schema for representing an existing Segment.

    **Attributes:**
    - `segment_id (int)`: Unique identifier for the segment.
    - `segment_name (str)`: Name of the segment.
    - `segment_description (Optional[str])`: Optional description of the segment.
    """
    segment_id: int
    segment_name: str
    segment_description: Optional[str] = None

class Customer(BaseSchema):
    """
    Schema for representing an existing Customer.

    **Attributes:**
    - `customer_id (int)`: Unique identifier for the customer.
    - `name (str)`: Name of the customer.
    - `email (str)`: Email address of the customer.
    - `subscription_id (int)`: ID of the associated subscription.
    - `location (Optional[str])`: Optional location of the customer.
    - `created_at (datetime)`: Timestamp when the customer was created.
    - `updated_at (datetime)`: Timestamp when the customer was last updated.
    """

    customer_id: int
    name: str
    email: str
    subscription_id: int
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CustomerCreate(BaseSchema):
    """
    Schema for creating a new Customer.

    **Attributes:**
    - `name (str)`: Name of the customer.
    - `email (str)`: Email address of the customer.
    - `location (Optional[str])`: Optional location of the customer.
    - `subscription_id (int)`: ID of the associated subscription.
    """

    name: str
    email: str
    location: Optional[str] = None
    #created_at: datetime
    #updated_at: datetime
    subscription_id: int


class EmailRequest(BaseModel):
    """
    Schema for the email request.

    **Attributes:**
    - `segment_name (str)`: Name of the customer segment.
    - `text_skeleton_1 (str)`: First email skeleton.
    - `text_skeleton_2 (str)`: Second email skeleton.
    - `ab_test_id_a (int)`: A/B test ID for variant A.
    - `ab_test_id_b (int)`: A/B test ID for variant B.
    """
    segment_name: str
    text_skeleton_1: str
    text_skeleton_2: str
    ab_test_id_a : int 
    ab_test_id_b : int

class CustomerSegmentCreate(BaseModel):
    """
    Schema for creating a new Customer-Segment relationship.
    """
    pass

class CustomerSegment(BaseModel):
    """
    Schema for representing an existing Customer-Segment relationship.

    **Attributes:**
    - `customer_segment_id (int)`: Unique identifier for the relationship.
    - `customer_id (int)`: ID of the customer.
    - `segment_id (int)`: ID of the segment.
    """
    customer_segment_id: int
    customer_id: int
    segment_id: int


class MovieCreate(BaseModel):
    """
    Schema for creating a new Movie.
    """
    pass

class Movie(BaseModel):
    """
    Schema for representing an existing Movie.

    **Attributes:**
    - `movie_id (int)`: Unique identifier for the movie.
    - `movie_name (str)`: Name of the movie.
    - `movie_rating (Optional[float])`: Optional rating of the movie.
    - `movie_duration (Optional[int])`: Optional duration of the movie.
    - `movie_genre (Optional[str])`: Optional genre of the movie.
    - `release_year (Optional[int])`: Optional release year of the movie.
    """
    movie_id: int
    movie_name: str
    movie_rating: Optional[float] = None
    movie_duration: Optional[int] = None
    movie_genre: Optional[str] = None
    release_year: Optional[int] = None



class EngagementCreate(BaseModel):
    """
    Schema for creating a new Engagement.
    """
    pass

class Engagement(BaseModel):
    """
    Schema for representing an existing Engagement.

    **Attributes:**
    - `engagement_id (int)`: Unique identifier for the engagement.
    - `customer_id (int)`: ID of the customer who engaged with the movie.
    - `movie_id (int)`: ID of the movie that the customer engaged with.
    - `session_date (datetime)`: Timestamp of the engagement.
    - `session_duration (int)`: Duration of the session in minutes.
    - `watched_fully (bool)`: Indicates if the movie was watched fully.
    - `like_status (Optional[str])`: Optional feedback status of the customer.
    """
    engagement_id: int
    customer_id: int
    movie_id: int
    session_date : datetime
    session_duration : int
    watched_fully: bool
    like_status: Optional[str] = None

class SubscriptionCreate(BaseModel):
    """
    Schema for creating a new Subscription.

    """
    pass

class Subscription(BaseModel):
    """
    Schema for representing an existing Subscription.

    **Attributes:**
    - `subscription_id (int)`: Unique identifier for the subscription.
    - `subscription_name (str)`: Name of the subscription plan.
    - `price (int)`: Price of the subscription.
    """
    subscription_id: int
    subscription_name: str
    price: int

class ABTestCreate(BaseModel):
    """
    Schema for creating a new A/B Test.

    """
    pass

class ABTest(BaseModel):
    """
    Schema for representing an existing A/B Test.

    **Attributes:**
    - `ab_test_id (int)`: Unique identifier for the A/B Test.
    - `goal (str)`: The goal of the test (e.g., 'Engagement', 'Subscription').
    - `targeting (str)`: Targeting criteria (e.g., 'genre', 'movie', 'package').
    - `test_variant (int)`: The variant ID for the test.
    - `text_skeleton (str)`: The text template for the test.
    """
    ab_test_id: int
    goal: str
    targeting: str
    test_variant: int
    text_skeleton: str


class ABTestResultCreate(BaseModel):
    """
    Schema for creating a new A/B Test Result.

    **Attributes:**
    - `experiment_id (int)`: ID of the experiment related to the result.
    - `customer_id (int)`: ID of the customer related to the result.
    - `clicked_link (bool)`: Whether the customer clicked the link in the test.
    """

    experiment_id: int
    customer_id: int
    clicked_link: bool

class ABTestResult(BaseModel):
    """
    Schema for representing an existing A/B Test Result.

    **Attributes:**
    - `result_id (int)`: Unique identifier for the result.
    - `ab_test_id (int)`: ID of the related A/B test.
    - `experiment_id (int)`: ID of the experiment related to the result.
    - `customer_id (int)`: ID of the customer related to the result.
    - `clicked_link (bool)`: Whether the customer clicked the test link.
    """
    result_id : int
    ab_test_id: int
    experiment_id: int
    customer_id: int
    clicked_link: bool



class ExperimentCreate(BaseModel):
    """
    Schema for creating a new Experiment.

    **Attributes:**
    - `p_value (float)`: P-value from the statistical test.
    """

    p_value: float


class Experiment(BaseModel):
    """
    Schema for representing an existing Experiment.

    **Attributes:**
    - `experiment_id (int)`: Unique identifier for the experiment.
    - `p_value (float)`: P-value indicating the statistical significance of the experiment.
    """
    experiment_id: int
    p_value: float