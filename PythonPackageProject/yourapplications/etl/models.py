from loguru import logger


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from database import Base, engine

Base= declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True)
    subscription_name = Column(String)
    price = Column(Integer)

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    release_year = Column(Integer)
    rating = Column(Float)
    

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


class Engagement(Base):
    __tablename__ = "engagements"
    
    engagement_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_id =  Column(Integer, ForeignKey("products.product_id"))
    session_duration = Column(Integer)
    session_date = Column(DateTime)
    device_type = Column(String)
    watched_fully = Column(Boolean)

    customer = relationship("Customer")
    prouct = relationship("Product")

class ABTest(Base):
    __tablename__ = "ab_tests"
    
    ab_test_id = Column(Integer, primary_key=True)
    test_variant = Column(Integer)
    test_goal = Column(String)


Base.metadata.create_all(engine)

