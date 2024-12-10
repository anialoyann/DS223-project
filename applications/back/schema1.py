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

    **Inherits:**
    - `SegmentBase`: Contains all base attributes.
    """
    pass

class Segment(BaseModel):
    """
    Schema for representing an existing Segment.

    **Attributes:**
    - `segment_id (int)`: Unique identifier for the segment.
    """
    segment_id: int
    segment_name: str
    segment_description: Optional[str] = None

class Customer(BaseSchema):
    """
    Schema for representing an existing Customer.
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
    - `subscription_id (int)`: ID of the subscription associated with the customer.
    """
    name: str
    email: str
    location: Optional[str] = None
    #created_at: datetime
    #updated_at: datetime
    subscription_id: int



class CustomerSegmentCreate(BaseModel):
    """
    Schema for creating a new Customer-Segment relationship.

    **Inherits:**
    - `CustomerSegmentBase`: Contains all base attributes.
    """
    pass

class CustomerSegment(BaseModel):
    """
    Schema for representing an existing Customer-Segment relationship.

    **Attributes:**
    - `customer_segment_id (int)`: Unique identifier for the relationship.
    """
    customer_segment_id: int
    customer_id: int
    segment_id: int


class MovieCreate(BaseModel):
    """
    Schema for creating a new Movie.

    **Inherits:**
    - `MovieBase`: Contains all base attributes.
    """
    pass

class Movie(BaseModel):
    """
    Schema for representing an existing Movie.

    **Attributes:**
    - `movie_id (int)`: Unique identifier for the movie.
    """
    movie_id: int
    movie_name: str
    movie_rating: Optional[float] = None
    movie_duration: Optional[int] = None
    movie_genre: Optional[str] = None
    release_year: Optional[int] = None


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
