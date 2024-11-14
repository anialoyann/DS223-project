from sqlalchemy import Column, Integer, String, Date, Float, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    subscription_type = Column(String)
    location = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class Engagement(Base):
    __tablename__ = "engagements"
    engagement_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    session_duration = Column(Integer)
    session_date = Column(Date)
    actions = Column(JSON)
    device_type = Column(String)
    customer = relationship("Customer")

class Segment(Base):
    __tablename__ = "segments"
    segment_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    criteria = Column(JSON)

class CustomerSegment(Base):
    __tablename__ = "customer_segments"
    customer_segment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))

class ABTest(Base):
    __tablename__ = "ab_tests"
    ab_test_id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))
    test_variant = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    result_metric = Column(String)

class TestResult(Base):
    __tablename__ = "test_results"
    test_result_id = Column(Integer, primary_key=True, index=True)
    ab_test_id = Column(Integer, ForeignKey("ab_tests.ab_test_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    engagement_change = Column(Float)
    retention_change = Column(Float)
