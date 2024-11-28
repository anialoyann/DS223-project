from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Base Schema for common fields
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True  # To convert SQLAlchemy models to Pydantic models

# Segment Schema
class SegmentBase(BaseSchema):
    segment_name: str
    segment_description: Optional[str] = None

class SegmentCreate(SegmentBase):
    pass

class Segment(SegmentBase):
    segment_id: int

# Customer Schema
class CustomerBase(BaseSchema):
    name: str
    email: str
    location: Optional[str] = None

class CustomerCreate(CustomerBase):
    subscription_id: int

class Customer(CustomerBase):
    customer_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# Customer Segment Schema
class CustomerSegmentBase(BaseSchema):
    customer_id: int
    segment_id: int

class CustomerSegmentCreate(CustomerSegmentBase):
    pass

class CustomerSegment(CustomerSegmentBase):
    customer_segment_id: int

# Movie Schema
class MovieBase(BaseSchema):
    movie_name: str
    movie_rating: Optional[float] = None
    movie_duration: Optional[int] = None
    movie_genre: Optional[str] = None
    release_year: Optional[int] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    movie_id: int

# Engagement Schema
class EngagementBase(BaseSchema):
    customer_id: int
    movie_id: int
    has_watched_fully: bool
    like_status: Optional[str] = None
    date_watched: Optional[str] = None

class EngagementCreate(EngagementBase):
    pass

class Engagement(EngagementBase):
    customer_movie_id: int

# Subscription Schema
class SubscriptionBase(BaseSchema):
    subscription_name: str
    price: int

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    subscription_id: int

# AB Test Schema
class ABTestBase(BaseSchema):
    goal: str
    targeting: str
    test_variant: int
    text_skeleton: str

class ABTestCreate(ABTestBase):
    pass

class ABTest(ABTestBase):
    ab_test_id: int

# AB Test Result Schema
class ABTestResultBase(BaseSchema):
    ab_test_id: int
    experiment_id: int  # Updated to include experiment_id
    customer_id: int
    clicked_link: bool
    time_spent_seconds: int

class ABTestResultCreate(ABTestResultBase):
    pass

class ABTestResult(ABTestResultBase):
    result_id: int

# Experiment Schema (New Model)
class ExperimentBase(BaseSchema):
    p_value: float

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    experiment_id: int
