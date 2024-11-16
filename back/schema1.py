from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Segment Schemas
class SegmentBase(BaseModel):
    segment_name: str
    segment_description: Optional[str]

class SegmentCreate(SegmentBase):
    pass

class Segment(SegmentBase):
    segment_id: int
    class Config:
        orm_mode = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    subscription_id: Optional[int]
    location: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

# Customer Segment Schemas
class CustomerSegmentBase(BaseModel):
    customer_id: int
    segment_id: int

class CustomerSegmentCreate(CustomerSegmentBase):
    pass

class CustomerSegment(CustomerSegmentBase):
    customer_segment_id: int
    class Config:
        orm_mode = True

# Movie Schemas
class MovieBase(BaseModel):
    movie_name: str
    movie_rating: Optional[float]
    movie_duration: Optional[int]
    movie_genre: Optional[str]
    release_year: Optional[int]

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    movie_id: int
    class Config:
        orm_mode = True

# Engagement Schemas
class EngagementBase(BaseModel):
    customer_id: int
    movie_id: int
    has_watched_fully: Optional[bool]
    like_status: Optional[str]
    date_watched: Optional[datetime]

class EngagementCreate(EngagementBase):
    pass

class Engagement(EngagementBase):
    customer_movie_id: int
    class Config:
        orm_mode = True

# Subscription Schemas
class SubscriptionBase(BaseModel):
    subscription_name: str
    price: int

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    subscription_id: int
    class Config:
        orm_mode = True

# AB Test Schemas
class ABTestBase(BaseModel):
    goal: str
    targeting: str
    test_variant: Optional[int]
    text_skeleton: Optional[str]

class ABTestCreate(ABTestBase):
    pass

class ABTest(ABTestBase):
    ab_test_id: int
    class Config:
        orm_mode = True

# AB Test Result Schemas
class ABTestResultBase(BaseModel):
    ab_test_id: int
    customer_id: int
    clicked_link: Optional[bool]
    time_spent_seconds: Optional[int]

class ABTestResultCreate(ABTestResultBase):
    pass

class ABTestResult(ABTestResultBase):
    result_id: int
    class Config:
        orm_mode = True
