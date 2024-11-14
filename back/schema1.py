from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    subscription_type: str
    location: str

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

# Engagement Schemas
class EngagementBase(BaseModel):
    customer_id: int
    session_duration: int
    session_date: date
    actions: dict
    device_type: str

class EngagementCreate(EngagementBase):
    pass

class EngagementUpdate(EngagementBase):
    pass

class Engagement(EngagementBase):
    engagement_id: int
    class Config:
        orm_mode = True

# Engagement Schemas
class EngagementBase(BaseModel):
    customer_id: int
    session_duration: int
    session_date: date
    actions: dict
    device_type: str

class EngagementCreate(EngagementBase):
    pass

class EngagementUpdate(EngagementBase):
    pass

class Engagement(EngagementBase):
    engagement_id: int
    class Config:
        orm_mode = True

# Segment Schemas
class SegmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    criteria: dict  # JSON data represented as a dictionary

class SegmentCreate(SegmentBase):
    pass

class SegmentUpdate(SegmentBase):
    pass

class Segment(SegmentBase):
    segment_id: int
    class Config:
        orm_mode = True

# CustomerSegment Schemas
class CustomerSegmentBase(BaseModel):
    customer_id: int
    segment_id: int

class CustomerSegmentCreate(CustomerSegmentBase):
    pass

class CustomerSegmentUpdate(CustomerSegmentBase):
    pass

class CustomerSegment(CustomerSegmentBase):
    customer_segment_id: int
    class Config:
        orm_mode = True

# ABTest Schemas
class ABTestBase(BaseModel):
    segment_id: int
    test_variant: str
    start_date: date
    end_date: date
    result_metric: str

class ABTestCreate(ABTestBase):
    pass

class ABTestUpdate(ABTestBase):
    pass

class ABTest(ABTestBase):
    ab_test_id: int
    class Config:
        orm_mode = True

# TestResult Schemas
class TestResultBase(BaseModel):
    ab_test_id: int
    customer_id: int
    engagement_change: float
    retention_change: float

class TestResultCreate(TestResultBase):
    pass

class TestResultUpdate(TestResultBase):
    pass

class TestResult(TestResultBase):
    test_result_id: int
    class Config:
        orm_mode = True