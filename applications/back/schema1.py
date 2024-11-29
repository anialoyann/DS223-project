from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Base Schema for common fields
class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.

    **Config:**
    - `orm_mode`: Enables compatibility with SQLAlchemy models for easy conversion.
    """
    class Config:
        orm_mode = True

# Segment Schema
class SegmentBase(BaseSchema):
    """
    Schema for the base structure of a Segment.

    **Attributes:**
    - `segment_name (str)`: Name of the segment.
    - `segment_description (Optional[str])`: Description of the segment (optional).
    """
    segment_name: str
    segment_description: Optional[str] = None

class SegmentCreate(SegmentBase):
    """
    Schema for creating a new Segment.

    **Inherits:**
    - `SegmentBase`: Contains all base attributes.
    """
    pass

class Segment(SegmentBase):
    """
    Schema for representing an existing Segment.

    **Attributes:**
    - `segment_id (int)`: Unique identifier for the segment.
    """
    segment_id: int

# Customer Schema
class CustomerBase(BaseSchema):
    """
    Schema for the base structure of a Customer.

    **Attributes:**
    - `name (str)`: Name of the customer.
    - `email (str)`: Unique email address of the customer.
    - `location (Optional[str])`: Location of the customer (optional).
    """
    name: str
    email: str
    location: Optional[str] = None

class CustomerCreate(CustomerBase):
    """
    Schema for creating a new Customer.

    **Attributes:**
    - `subscription_id (int)`: ID of the subscription associated with the customer.
    """
    subscription_id: int

class Customer(CustomerBase):
    """
    Schema for representing an existing Customer.

    **Attributes:**
    - `customer_id (int)`: Unique identifier for the customer.
    - `created_at (Optional[str])`: Timestamp when the customer was created (optional).
    - `updated_at (Optional[str])`: Timestamp when the customer was last updated (optional).
    """
    customer_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# Customer Segment Schema
class CustomerSegmentBase(BaseSchema):
    """
    Schema for the base structure of a Customer-Segment relationship.

    **Attributes:**
    - `customer_id (int)`: ID of the customer in the relationship.
    - `segment_id (int)`: ID of the segment in the relationship.
    """
    customer_id: int
    segment_id: int

class CustomerSegmentCreate(CustomerSegmentBase):
    """
    Schema for creating a new Customer-Segment relationship.

    **Inherits:**
    - `CustomerSegmentBase`: Contains all base attributes.
    """
    pass

class CustomerSegment(CustomerSegmentBase):
    """
    Schema for representing an existing Customer-Segment relationship.

    **Attributes:**
    - `customer_segment_id (int)`: Unique identifier for the relationship.
    """
    customer_segment_id: int

# Movie Schema
class MovieBase(BaseSchema):
    """
    Schema for the base structure of a Movie.

    **Attributes:**
    - `movie_name (str)`: Name of the movie.
    - `movie_rating (Optional[float])`: Rating of the movie (optional).
    - `movie_duration (Optional[int])`: Duration of the movie in minutes (optional).
    - `movie_genre (Optional[str])`: Genre of the movie (optional).
    - `release_year (Optional[int])`: Year the movie was released (optional).
    """
    movie_name: str
    movie_rating: Optional[float] = None
    movie_duration: Optional[int] = None
    movie_genre: Optional[str] = None
    release_year: Optional[int] = None

class MovieCreate(MovieBase):
    """
    Schema for creating a new Movie.

    **Inherits:**
    - `MovieBase`: Contains all base attributes.
    """
    pass

class Movie(MovieBase):
    """
    Schema for representing an existing Movie.

    **Attributes:**
    - `movie_id (int)`: Unique identifier for the movie.
    """
    movie_id: int

# Engagement Schema
class EngagementBase(BaseSchema):
    """
    Schema for the base structure of a Customer's Engagement with a Movie.

    **Attributes:**
    - `customer_id (int)`: ID of the customer involved in the engagement.
    - `movie_id (int)`: ID of the movie involved in the engagement.
    - `has_watched_fully (bool)`: Indicates if the movie was fully watched.
    - `like_status (Optional[str])`: Feedback from the customer (optional).
    - `date_watched (Optional[str])`: Timestamp of when the movie was watched (optional).
    """
    customer_id: int
    movie_id: int
    has_watched_fully: bool
    like_status: Optional[str] = None
    date_watched: Optional[str] = None

class EngagementCreate(EngagementBase):
    """
    Schema for creating a new Engagement.

    **Inherits:**
    - `EngagementBase`: Contains all base attributes.
    """
    pass

class Engagement(EngagementBase):
    """
    Schema for representing an existing Engagement.

    **Attributes:**
    - `customer_movie_id (int)`: Unique identifier for the engagement.
    """
    customer_movie_id: int

# Subscription Schema
class SubscriptionBase(BaseSchema):
    """
    Schema for the base structure of a Subscription.

    **Attributes:**
    - `subscription_name (str)`: Name of the subscription.
    - `price (int)`: Cost of the subscription.
    """
    subscription_name: str
    price: int

class SubscriptionCreate(SubscriptionBase):
    """
    Schema for creating a new Subscription.

    **Inherits:**
    - `SubscriptionBase`: Contains all base attributes.
    """
    pass

class Subscription(SubscriptionBase):
    """
    Schema for representing an existing Subscription.

    **Attributes:**
    - `subscription_id (int)`: Unique identifier for the subscription.
    """
    subscription_id: int

# AB Test Schema
class ABTestBase(BaseSchema):
    """
    Schema for the base structure of an A/B Test.

    **Attributes:**
    - `goal (str)`: Goal of the A/B Test (e.g., 'Engagement' or 'Subscription').
    - `targeting (str)`: Targeting criteria (e.g., 'genre', 'movie', or 'package').
    - `test_variant (int)`: Variant identifier for the test.
    - `text_skeleton (str)`: Template for the email body in the test.
    """
    goal: str
    targeting: str
    test_variant: int
    text_skeleton: str

class ABTestCreate(ABTestBase):
    """
    Schema for creating a new A/B Test.

    **Inherits:**
    - `ABTestBase`: Contains all base attributes.
    """
    pass

class ABTest(ABTestBase):
    """
    Schema for representing an existing A/B Test.

    **Attributes:**
    - `ab_test_id (int)`: Unique identifier for the A/B Test.
    """
    ab_test_id: int

# AB Test Result Schema
class ABTestResultBase(BaseSchema):
    """
    Schema for the base structure of an A/B Test Result.

    **Attributes:**
    - `ab_test_id (int)`: ID of the associated A/B Test.
    - `experiment_id (int)`: ID of the associated Experiment.
    - `customer_id (int)`: ID of the customer involved in the test.
    - `clicked_link (bool)`: Indicates if the customer clicked the link.
    - `time_spent_seconds (int)`: Time spent interacting with the test.
    """
    ab_test_id: int
    experiment_id: int
    customer_id: int
    clicked_link: bool
    time_spent_seconds: int

class ABTestResultCreate(ABTestResultBase):
    """
    Schema for creating a new A/B Test Result.

    **Inherits:**
    - `ABTestResultBase`: Contains all base attributes.
    """
    pass

class ABTestResult(ABTestResultBase):
    """
    Schema for representing an existing A/B Test Result.

    **Attributes:**
    - `result_id (int)`: Unique identifier for the result.
    """
    result_id: int

# Experiment Schema
class ExperimentBase(BaseSchema):
    """
    Schema for the base structure of an Experiment.

    **Attributes:**
    - `p_value (float)`: Statistical p-value representing the experiment's significance.
    """
    p_value: float

class ExperimentCreate(ExperimentBase):
    """
    Schema for creating a new Experiment.

    **Inherits:**
    - `ExperimentBase`: Contains all base attributes.
    """
    pass

class Experiment(ExperimentBase):
    """
    Schema for representing an existing Experiment.

    **Attributes:**
    - `experiment_id (int)`: Unique identifier for the experiment.
    """
    experiment_id: int
