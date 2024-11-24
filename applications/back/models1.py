from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database1 import Base

# Segments Model
class Segment(Base):
    __tablename__ = "segments"
    segment_id = Column(Integer, primary_key=True, index=True)
    segment_name = Column(String, nullable=False)
    segment_description = Column(Text)
    customers = relationship("CustomerSegment", back_populates="segment")

# Customers Model
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id"))
    location = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    segments = relationship("CustomerSegment", back_populates="customer")
    engagements = relationship("Engagement", back_populates="customer")
    
# Customer Segments Model
class CustomerSegment(Base):
    __tablename__ = "customer_segments"
    customer_segment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))
    customer = relationship("Customer", back_populates="segments")
    segment = relationship("Segment", back_populates="customers")

# Movies Model
class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True, index=True)
    movie_name = Column(String, nullable=False)
    movie_rating = Column(Float)
    movie_duration = Column(Integer)
    movie_genre = Column(String)
    release_year = Column(Integer)

# Engagements Model
class Engagement(Base):
    __tablename__ = "engagements"
    customer_movie_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    has_watched_fully = Column(Boolean)
    like_status = Column(String)
    date_watched = Column(DateTime)
    customer = relationship("Customer", back_populates="engagements")
    movie = relationship("Movie")

# Subscriptions Model
class Subscription(Base):
    __tablename__ = "subscriptions"
    subscription_id = Column(Integer, primary_key=True, index=True)
    subscription_name = Column(String, nullable=False)
    price = Column(Integer)

# AB Tests Model
class ABTest(Base):
    __tablename__ = "ab_tests"
    ab_test_id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, nullable=False)  # 'Engagement' or 'Subscription'
    targeting = Column(String, nullable=False)  # 'genre', 'movie', or 'package'
    test_variant = Column(Integer)  # A/B Test variant identifier
    text_skeleton = Column(Text)  # Text template used in the A/B Test
    results = relationship("ABTestResult", back_populates="ab_test")

# AB Test Results Model
class ABTestResult(Base):
    __tablename__ = "ab_test_results"
    result_id = Column(Integer, primary_key=True, index=True)
    ab_test_id = Column(Integer, ForeignKey("ab_tests.ab_test_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    clicked_link = Column(Boolean)
    time_spent_seconds = Column(Integer)
    ab_test = relationship("ABTest", back_populates="results")
    customer = relationship("Customer")
