from loguru import logger


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from database import Base, engine

Base= declarative_base()
#ADDING THIS JUST TO COMMIT PLEASE
class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True)
    subscription_name = Column(String)
    price = Column(Integer)

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String)
    release_year = Column(Integer)
    movie_duration = Column(Integer)
    movie_rating = Column(Float)
    movie_genre = Column(String)

class Customer(Base):
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
    __tablename__ = "segments"

    segment_id = Column(Integer, primary_key=True)
    segment_name = Column(String)
    segment_description = Column(Text)

class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    customer_segment_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    segment_id = Column(Integer, ForeignKey("segments.segment_id"))

    customer = relationship("Customer")
    segment = relationship("Segment")

class Engagement(Base):
    __tablename__ = "engagements"
    
    engagement_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    movie_id =  Column(Integer, ForeignKey("movies.movie_id"))
    session_duration = Column(Integer)
    session_date = Column(DateTime)
    device_type = Column(String)
    watched_fully = Column(Boolean)
    like_status = Column(String)

    customer = relationship("Customer")
    movie = relationship("Movie")

class ABTest(Base):
    __tablename__ = "ab_tests"
    
    ab_test_id = Column(Integer, primary_key=True)
    goal = Column(String)
    targeting = Column(String)
    test_variant = Column(Integer)
    text_skeleton = Column(Text)

class ABTest_Result(Base):
    __tablename__ = "ab_test_results"

    result_id = Column(Integer, primary_key=True)
    ab_test_id = Column(Integer, ForeignKey("ab_tests.ab_test_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    clicked_link = Column(Boolean)
    time_spent_seconds = Column(Integer)

    customer = relationship("Customer")
    abtest = relationship("ABTest")

Base.metadata.create_all(engine)

