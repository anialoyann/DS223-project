from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from back.database1 import*
import back.models1 as models1, back.schema1 as schemas

# Creating database tables
models1.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# CRUD for Segments
@app.post("/segments/", response_model=schemas.Segment)
def create_segment(segment: schemas.SegmentCreate, db: Session = Depends(get_db)):
    db_segment = models1.Segment(**segment.dict())
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment

@app.get("/segments/", response_model=list[schemas.Segment])
def read_segments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.Segment).offset(skip).limit(limit).all()

# CRUD for Customers
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models1.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.Customer).offset(skip).limit(limit).all()

# CRUD for Customer Segments
@app.post("/customer_segments/", response_model=schemas.CustomerSegment)
def create_customer_segment(customer_segment: schemas.CustomerSegmentCreate, db: Session = Depends(get_db)):
    db_customer_segment = models1.CustomerSegment(**customer_segment.dict())
    db.add(db_customer_segment)
    db.commit()
    db.refresh(db_customer_segment)
    return db_customer_segment

@app.get("/customer_segments/", response_model=list[schemas.CustomerSegment])
def read_customer_segments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.CustomerSegment).offset(skip).limit(limit).all()

# CRUD for Movies
@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models1.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.Movie).offset(skip).limit(limit).all()

# CRUD for Engagements
@app.post("/engagements/", response_model=schemas.Engagement)
def create_engagement(engagement: schemas.EngagementCreate, db: Session = Depends(get_db)):
    db_engagement = models1.Engagement(**engagement.dict())
    db.add(db_engagement)
    db.commit()
    db.refresh(db_engagement)
    return db_engagement

@app.get("/engagements/", response_model=list[schemas.Engagement])
def read_engagements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.Engagement).offset(skip).limit(limit).all()

# CRUD for Subscriptions
@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = models1.Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.get("/subscriptions/", response_model=list[schemas.Subscription])
def read_subscriptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.Subscription).offset(skip).limit(limit).all()

# CRUD for AB Tests
@app.post("/ab_tests/", response_model=schemas.ABTest)
def create_ab_test(ab_test: schemas.ABTestCreate, db: Session = Depends(get_db)):
    db_ab_test = models1.ABTest(**ab_test.dict())
    db.add(db_ab_test)
    db.commit()
    db.refresh(db_ab_test)
    return db_ab_test

@app.get("/ab_tests/", response_model=list[schemas.ABTest])
def read_ab_tests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.ABTest).offset(skip).limit(limit).all()

# CRUD for AB Test Results
@app.post("/ab_test_results/", response_model=schemas.ABTestResult)
def create_ab_test_result(ab_test_result: schemas.ABTestResultCreate, db: Session = Depends(get_db)):
    db_ab_test_result = models1.ABTestResult(**ab_test_result.dict())
    db.add(db_ab_test_result)
    db.commit()
    db.refresh(db_ab_test_result)
    return db_ab_test_result

@app.get("/ab_test_results/", response_model=list[schemas.ABTestResult])
def read_ab_test_results(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models1.ABTestResult).offset(skip).limit(limit).all()
