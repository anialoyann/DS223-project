from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database1 import engine, SessionLocal
import models1 as models1,schema1 as schemas
from email_utils import send_email 
from datetime import datetime, timezone
import pandas as pd
import requests
from loguru import logger
import uuid

# Creating database tables
models1.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/test-send-email")
async def test_send_email():
    """
    Send a test email.

    **Parameters:**
    - No parameters for this test endpoint.

    **Returns:**
    - `message (str)`: A message indicating the test email was sent successfully.

    **Raises:**
    - `HTTPException`: If there's an issue with sending the email, it raises a 500 error.
    """
    recipient_email = ["ani_aloyan2@edu.aua.am"]  
    subject = "Test Email"
    body = "This is a test email sent from FastAPI without using the database."

    # Send the email
    send_email(recipient_email, subject, body)
    
    return {"message": "Test email sent successfully!"}



import logging

# Set up logging configuration
logging.basicConfig(
    filename="email_sending.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Dependency to get DB session
def get_db():
    """
    Dependency that provides a database session.

    **Returns:**
    - `db (Session)`: The database session.

    **Raises:**
    - None.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base Root
@app.get("/")
def read_root():
    """
    Root endpoint for checking if the FastAPI application is working.
    
    **Parameters:**
    - No parameters for this root endpoint.
    
    **Returns:**
    - `message (str)`: A simple welcome message confirming that the app is working.
    """
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/send-emails")
async def send_emails(request: schemas.EmailRequest, db: Session = Depends(get_db)):
    """
    Send personalized emails to customers in the selected segment and track performance.

    **Parameters:**
    - `request (schemas.EmailRequest)`: The request body containing the following data:
        - `segment_name (str)`: The name of the customer segment.
        - `text_skeleton_1 (str)`: The first email skeleton message.
        - `text_skeleton_2 (str)`: The second email skeleton message.
        - `ab_test_id_a (int)`: The ID of the A/B test for Variant A.
        - `ab_test_id_b (int)`: The ID of the A/B test for Variant B.

    **Returns:**
    - `message (str)`: Success message with the count of emails sent.

    **Raises:**
    - `HTTPException (404)`: If the A/B test IDs do not exist or no customers are found for the segment.
    - `HTTPException (500)`: For any unexpected errors.
    """
    segment_name = request.segment_name
    text_skeleton_1 = request.text_skeleton_1
    text_skeleton_2 = request.text_skeleton_2
    ab_test_id_a = request.ab_test_id_a  # Passed from the frontend (Variant A)
    ab_test_id_b = request.ab_test_id_b  # Passed from the frontend (Variant B)

    try:
        # Validate both A/B test IDs exist
        for ab_test_id in [ab_test_id_a, ab_test_id_b]:
            ab_test = db.query(models1.ABTest).filter(models1.ABTest.ab_test_id == ab_test_id).first()
            if not ab_test:
                raise HTTPException(status_code=404, detail=f"AB Test with ID {ab_test_id} not found.")

        # Insert a new experiment row with a NULL p-value
        new_experiment = models1.Experiment(p_value=float(1))
        db.add(new_experiment)
        db.commit()
        db.refresh(new_experiment)
        experiment_id = new_experiment.experiment_id  # Retrieve the generated experiment ID

        # Fetch target customers
        target_customers = (
            db.query(models1.Customer)
            .join(models1.CustomerSegment, models1.Customer.customer_id == models1.CustomerSegment.customer_id)
            .join(models1.Segment, models1.CustomerSegment.segment_id == models1.Segment.segment_id)
            .filter(
                models1.Segment.segment_name.ilike(segment_name),
                models1.Customer.customer_id > 2000
            )
            .all()
        )

        if not target_customers:
            raise HTTPException(
                status_code=404, detail=f"No customers found for the segment '{segment_name}'."
            )

        # Split customers into two groups for A/B testing
        mid_index = len(target_customers) // 2
        group_a = target_customers[:mid_index]
        group_b = target_customers[mid_index:]

        # Add tracking links and send emails
        emails_sent = 0

        for idx, (group, ab_test_id, skeleton) in enumerate([
            (group_a, ab_test_id_a, text_skeleton_1),
            (group_b, ab_test_id_b, text_skeleton_2),
        ]):
            for customer in group:
                try:
                    # Generate tracking link
                    tracking_token = str(uuid.uuid4())
                    tracking_url = (
                        f"http://localhost:8000/track/click/{ab_test_id}/{experiment_id}/{customer.customer_id}/{tracking_token}"
                    )

                    # Insert click tracking data into ab_test_results
                    ab_test_result = models1.ABTestResult(
                        ab_test_id=ab_test_id,
                        experiment_id=experiment_id,
                        customer_id=customer.customer_id,
                        clicked_link=False,  # Default to False; updated upon click
                    )
                    db.add(ab_test_result)

                    # Send email
                    first_name = customer.name.split(" ")[0]
                    email_body = f"{skeleton}\n\nClick here to learn more: {tracking_url}"
                    send_email(
                        recipient_email=[customer.email],
                        subject="Exciting News",
                        body=f"Hi {first_name}!\n\n{email_body}",
                    )
                    logger.info(f"Email sent successfully to {customer.email}.")
                    emails_sent += 1
                except Exception as e:
                    logger.warning(f"Failed to send email to {customer.email}: {e}")

        # Commit tracking data to the database
        db.commit()

        return {"message": f"Emails sent successfully to {emails_sent} customers."}

    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



@app.get("/track/click/{ab_test_id}/{experiment_id}/{customer_id}/{click_token}")
async def track_click(
    ab_test_id: int,
    experiment_id: int,
    customer_id: int,
    click_token: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint to track a click event for a specific customer in an A/B test.

    **Parameters:**
    - `ab_test_id (int)`: The ID of the A/B test.
    - `experiment_id (int)`: The ID of the experiment.
    - `customer_id (int)`: The ID of the customer.
    - `click_token (str)`: The unique token for tracking the click.

    **Returns:**
    - Success message if the click is tracked successfully.

    **Raises:**
    - `HTTPException (404)`: If no matching record is found.
    - `HTTPException (400)`: If the click has already been tracked.
    """
    try:
        # Fetch the click record
        click_record = db.query(models1.ABTestResult).filter(
            models1.ABTestResult.ab_test_id == ab_test_id,
            models1.ABTestResult.experiment_id == experiment_id,
            models1.ABTestResult.customer_id == customer_id,
        ).first()

        if not click_record:
            raise HTTPException(
                status_code=404, 
                detail=f"No click record found for ab_test_id={ab_test_id}, experiment_id={experiment_id}, customer_id={customer_id}."
            )

        # Check if the click has already been tracked
        if click_record.clicked_link:
            raise HTTPException(
                status_code=400,
                detail="Click has already been tracked for this customer."
            )

        # Update the record to mark the click
        click_record.clicked_link = True
        db.commit()

        return {"message": "Click tracked successfully"}

    except HTTPException as http_exc:
        logger.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while tracking the click."
        )


# CRUD for Segments
@app.post("/segments/", response_model=schemas.Segment)
def create_segment(segment: schemas.SegmentCreate, db: Session = Depends(get_db)):
    """
    Create a new segment.
    
    **Parameters:**
    - `segment (SegmentCreate)`: The segment data to create. This includes:
        - `segment_name (str)`: The name of the segment (required).
        - `segment_description (str, optional)`: A description of the segment (optional).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - `Segment`: The newly created segment's details, including the `segment_id`.
    """
    db_segment = models1.Segment(**segment.dict())
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment

@app.get("/segments/", response_model=list[schemas.Segment])
def read_segments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of segments with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of segments from the database.
    """
    return db.query(models1.Segment).offset(skip).limit(limit).all()


@app.get("/experiments/", response_model=list[schemas.Experiment])
def read_segments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of segments with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of segments from the database.
    """
    return db.query(models1.Experiment).offset(skip).limit(limit).all()


from sqlalchemy import text
from sqlalchemy.orm import Session

# CRUD for Customers
@app.post("/customers/")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer.
    
    **Parameters:**
    - `customer (CustomerCreate)`: The customer data to create. This includes:
        - `name (str)`: Customer's name.
        - `email (str)`: Customer's email address.
        - `subscription_id (str)`: Customer's subscription ID.
        - `location (str)`: Customer's location.
    
    **Returns:**
    - `Customer`: The newly created customer's details.
    """
    new_customer = models1.Customer(
        name=customer.name,
        email=customer.email,
        subscription_id=customer.subscription_id,
        location=customer.location
    )
    db.add(new_customer)
    db.commit()
    return schemas.Customer(
        customer_id=new_customer.customer_id,
        name=new_customer.name,
        email=new_customer.email,
        subscription_id=new_customer.subscription_id,
        location=new_customer.location,
        created_at=new_customer.created_at,
        updated_at=new_customer.updated_at
    )

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of customers with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of customers from the database.
    """
    return db.query(models1.Customer).offset(skip).limit(limit).all()

# CRUD for Customer Segments
@app.post("/customer_segments/", response_model=schemas.CustomerSegment)
def create_customer_segment(customer_segment: schemas.CustomerSegmentCreate, db: Session = Depends(get_db)):
    """
    Create a new customer segment.
    
    **Parameters:**
    - `customer_segment (CustomerSegmentCreate)`: The customer segment data to create. This includes:
        - `customer_id (int)`: The ID of the customer (required).
        - `segment_id (int)`: The ID of the segment (required).
    
    **Returns:**
    - `CustomerSegment`: The newly created customer segment's details.
    """
    db_customer_segment = models1.CustomerSegment(**customer_segment.dict())
    db.add(db_customer_segment)
    db.commit()
    db.refresh(db_customer_segment)
    return db_customer_segment

@app.get("/customer_segments/", response_model=list[schemas.CustomerSegment])
def read_customer_segments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of customer segments with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of customer segments from the database.
    """
    return db.query(models1.CustomerSegment).offset(skip).limit(limit).all()

# CRUD for Movies
@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie.
    
    **Parameters:**
    - `movie (MovieCreate)`: The movie data to create. This includes:
        - `movie_name (str)`: The name of the movie (required).
        - `movie_rating (float, optional)`: The rating of the movie (optional).
        - `movie_duration (int, optional)`: The duration of the movie (optional).
        - `movie_genre (str, optional)`: The genre of the movie (optional).
        - `release_year (int, optional)`: The release year of the movie (optional).
    
    **Returns:**
    - `Movie`: The newly created movie's details, including `movie_id`.
    """

    db_movie = models1.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of movies with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of movies from the database.
    """
    return db.query(models1.Movie).offset(skip).limit(limit).all()

# CRUD for Engagements
@app.post("/engagements/", response_model=schemas.Engagement)
def create_engagement(engagement: schemas.EngagementCreate, db: Session = Depends(get_db)):
    """
    Create a new engagement record.
    
    **Parameters:**
    - `engagement (EngagementCreate)`: The engagement data to create. This includes:
        - `customer_id (int)`: The ID of the customer (required).
        - `movie_id (int)`: The ID of the movie (required).
        - `watched_fully (bool)`: Whether the customer has watched the movie fully (required).
        - `like_status (str, optional)`: The like status of the movie (optional).
        - `date_watched (str, optional)`: The date when the movie was watched (optional).
    
    **Returns:**
    - `Engagement`: The newly created engagement record details.
    
    **Raises:**
    - `HTTPException`: If there's an error with the database operation, raises a 500 error.
    """
    db_engagement = models1.Engagement(**engagement.dict())
    db.add(db_engagement)
    db.commit()
    db.refresh(db_engagement)
    return db_engagement

@app.get("/engagements/", response_model=list[schemas.Engagement])
def read_engagements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of engagements with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of engagement records from the database.
    
    **Raises:**
    - `HTTPException`: If there's an issue retrieving the records, raises a 500 error.
    """

    return db.query(models1.Engagement).offset(skip).limit(limit).all()

# CRUD for Subscriptions
@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    """
    Create a new subscription record.
    
    **Parameters:**
    - `subscription (SubscriptionCreate)`: The subscription data to create. This includes:
        - `subscription_name (str)`: The name of the subscription package (required).
        - `price (int)`: The price of the subscription (required).
    
    **Returns:**
    - `Subscription`: The newly created subscription record details.
    
    **Raises:**
    - `HTTPException`: If there's an error with the database operation, raises a 500 error.
    """
    db_subscription = models1.Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.get("/subscriptions/", response_model=list[schemas.Subscription])
def read_subscriptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of subscriptions with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of subscription records from the database.
    
    **Raises:**
    - `HTTPException`: If there's an issue retrieving the records, raises a 500 error.
    """
    return db.query(models1.Subscription).offset(skip).limit(limit).all()

# CRUD for AB Tests
@app.post("/ab_tests/", response_model=schemas.ABTest)
def create_ab_test(ab_test: schemas.ABTestCreate, db: Session = Depends(get_db)):
    """
    Create a new A/B test record.
    
    **Parameters:**
    - `ab_test (ABTestCreate)`: The A/B test data to create. This includes:
        - `goal (str)`: The goal of the A/B test (e.g., 'Engagement' or 'Subscription').
        - `targeting (str)`: The targeting criteria (e.g., 'genre', 'movie', 'package').
        - `test_variant (int)`: The variant identifier for A/B testing (required).
        - `text_skeleton (str)`: The template for the test, including variants (required).
    
    **Returns:**
    - `ABTest`: The newly created A/B test record details.
    
    **Raises:**
    - `HTTPException`: If there's an error with the database operation, raises a 500 error.
    """
    db_ab_test = models1.ABTest(**ab_test.dict())
    db.add(db_ab_test)
    db.commit()
    db.refresh(db_ab_test)
    return db_ab_test

@app.get("/ab_tests/", response_model=list[schemas.ABTest])
def read_ab_tests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of A/B tests with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of A/B test records from the database.
    
    **Raises:**
    - `HTTPException`: If there's an issue retrieving the records, raises a 500 error.
    """
    return db.query(models1.ABTest).offset(skip).limit(limit).all()

# CRUD for AB Test Results
@app.post("/ab_test_results/", response_model=schemas.ABTestResult)
def create_ab_test_result(ab_test_result: schemas.ABTestResultCreate, db: Session = Depends(get_db)):
    """
    Create a new A/B test result record.
    
    **Parameters:**
    - `ab_test_result (ABTestResultCreate)`: The A/B test result data to create. This includes:
        - `ab_test_id (int)`: The ID of the A/B test (required).
        - `customer_id (int)`: The ID of the customer who participated in the test (required).
        - `clicked_link (bool)`: Whether the customer clicked the link (required).
    
    **Returns:**
    - `ABTestResult`: The newly created A/B test result record details.
    
    **Raises:**
    - `HTTPException`: If there's an error with the database operation, raises a 500 error.
    """
    db_ab_test_result = models1.ABTestResult(**ab_test_result.dict())
    db.add(db_ab_test_result)
    db.commit()
    db.refresh(db_ab_test_result)
    return db_ab_test_result

@app.get("/ab_test_results/", response_model=list[schemas.ABTestResult])
def read_ab_test_results(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """
    Fetch a list of A/B test results with pagination.
    
    **Parameters:**
    - `skip (int, optional)`: The number of records to skip (default is 0).
    - `limit (int, optional)`: The number of records to return (default is 10).
    - `db (Session, optional)`: The database session provided by dependency injection.
    
    **Returns:**
    - A list of A/B test result records from the database.
    
    **Raises:**
    - `HTTPException`: If there's an issue retrieving the records, raises a 500 error.
    """
    return db.query(models1.ABTestResult).offset(skip).limit(limit).all()

