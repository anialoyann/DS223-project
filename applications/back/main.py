from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database1 import engine, SessionLocal
import models1 as models1,schema1 as schemas
from email_utils import send_email 
from datetime import datetime, timezone


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

# Dependency to get DB session
def get_db():
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
    - `message`: A simple welcome message confirming that the app is working.
    """
    return {"message": "Welcome to the FastAPI application!"}

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

from sqlalchemy import text
from sqlalchemy.orm import Session

# CRUD for Customers
@app.post("/customers/")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
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
    - `db (Session, optional)`: The database session provided by dependency injection.
    
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
    - `db (Session, optional)`: The database session provided by dependency injection.
    
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
    - `db (Session, optional)`: The database session provided by dependency injection.
    
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
    - `db (Session, optional)`: The database session provided by dependency injection.
    
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
    - `db (Session, optional)`: The database session provided by dependency injection.
    
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
    - `db (Session, optional)`: The database session provided by dependency injection.
    
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
def read_ab_test_results(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
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

# Endpoint for running an A/B test for a subscription goal
@app.post("/run_ab_test_subscription/")
async def run_ab_test_subscription(
    segment_id: int, package_type: str, text_a: str, text_b: str, db: Session = Depends(get_db)
):
    """
    Run an A/B test for a subscription goal.

    **Parameters:**
    - `segment_id (int)`: The ID of the segment to target (required).
    - `package_type (str)`: The type of subscription package (required).
    - `text_a (str)`: Text for variant A of the test (required).
    - `text_b (str)`: Text for variant B of the test (required).
    - `db (Session, optional)`: The database session provided by dependency injection.

    **Returns:**
    - `message (str)`: A message confirming the creation of the A/B test and that emails have been sent.
    - `ab_test_id (int)`: The ID of the created A/B test.

    **Raises:**
    - `HTTPException`: If the segment is not found, raises a 404 error.
    """
    segment = db.query(models1.Segment).filter(models1.Segment.segment_id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

   
    ab_test = models1.ABTest(
        goal="Subscription",
        targeting=f"Package Type: {package_type}",
        test_variant=1,  # Variant identifier
        text_skeleton=f"Variant A: {text_a}, Variant B: {text_b}",
    )
    db.add(ab_test)
    db.commit()
    db.refresh(ab_test)

    
    text_a_entry = models1.Text(content=text_a)
    text_b_entry = models1.Text(content=text_b)
    db.add(text_a_entry)
    db.add(text_b_entry)
    db.commit()

    # Link the saved texts to the A/B test
    ab_test.test_variant = 1  # A/B test variant identifier for tracking
    db.commit()

    customers_in_segment = db.query(models1.Customer).join(models1.CustomerSegment).filter(
        models1.CustomerSegment.segment_id == segment_id).all()

    # Collect all customer emails
    recipient_emails = [customer.email for customer in customers_in_segment]
    
    if not recipient_emails:
        raise HTTPException(status_code=404, detail="No valid email addresses found")

    # Send the email with the appropriate subject and body
    send_email(
        recipient_email=recipient_emails,
        subject="Your A/B Test: Subscription Variant A/B",
        body=f"Variant A: {text_a}\nVariant B: {text_b}"
    )

    return {"message": "Subscription A/B test created and emails sent to segment", "ab_test_id": ab_test.ab_test_id}

# Endpoint for running an A/B test for engagement (genre or movie)
@app.post("/run_ab_test_engagement/")
async def run_ab_test_engagement(
    segment_id: int, target_type: str, target_value: str, text_a: str, text_b: str, db: Session = Depends(get_db)
):
    """
    Run an A/B test for engagement (genre or movie).

    **Parameters:**
    - `segment_id (int)`: The ID of the segment to target (required).
    - `target_type (str)`: The target type for engagement (e.g., 'genre', 'movie').
    - `target_value (str)`: The value for the target type (e.g., 'Action', 'Comedy').
    - `text_a (str)`: Text for variant A of the test (required).
    - `text_b (str)`: Text for variant B of the test (required).
    - `db (Session, optional)`: The database session provided by dependency injection.

    **Returns:**
    - `message (str)`: A message confirming the creation of the A/B test and that emails have been sent.
    - `ab_test_id (int)`: The ID of the created A/B test.

    **Raises:**
    - `HTTPException`: If the segment is not found, raises a 404 error.
    """
    segment = db.query(models1.Segment).filter(models1.Segment.segment_id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

    # Create A/B test for engagement goal
    ab_test = models1.ABTest(
        goal="Engagement",
        targeting=f"{target_type}: {target_value}",
        test_variant=2,  # Variant identifier
        text_skeleton=f"Variant A: {text_a}, Variant B: {text_b}",
    )
    db.add(ab_test)
    db.commit()
    db.refresh(ab_test)

    # Save texts for A/B testing
    text_a_entry = models1.Text(content=text_a)
    text_b_entry = models1.Text(content=text_b)
    db.add(text_a_entry)
    db.add(text_b_entry)
    db.commit()

    # Link the saved texts to the A/B test
    ab_test.test_variant = 2  # Variant identifier for tracking
    db.commit()

    # Retrieve the customer emails for the segment
    customers_in_segment = db.query(models1.Customer).join(models1.CustomerSegment).filter(
        models1.CustomerSegment.segment_id == segment_id).all()

    recipient_emails = [customer.email for customer in customers_in_segment]

    if not recipient_emails:
        raise HTTPException(status_code=404, detail="No valid email addresses found")


    send_email(
        recipient_email=recipient_emails,
        subject="Your A/B Test: Engagement Variant A/B",
        body=f"Variant A: {text_a}\nVariant B: {text_b}"
    )

    return {"message": "Engagement A/B test created and emails sent to segment", "ab_test_id": ab_test.ab_test_id}


@app.post("/send_email/")
async def send_email_to_customer(
    customer_id: int, 
    ab_test_id: int, 
    experiment_id: int, 
    db: Session = Depends(get_db)
):
    """
    Sends an email to a customer with a tracking link for A/B testing.

    This endpoint retrieves the customer's email from the database, 
    generates a tracking URL with a unique token, and sends the email 
    with the A/B test tracking link.

    **Parameters:**
    - `customer_id (int)`: The ID of the customer to whom the email will be sent.
    - `ab_test_id (int)`: The ID of the A/B test associated with the email.
    - `experiment_id (int)`: The ID of the experiment within the A/B test.
    - `db (Session)`: The database session to query the database.

    **Returns:**
    - A success message confirming the email was sent.

    **Raises:**
    - `HTTPException`: If the customer cannot be found in the database, a 404 error will be raised.
    """
    customer = db.query(models1.Customer).filter(models1.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    recipient_email = [customer.email]

    send_email(
        db=db,
        recipient_email=recipient_email,
        ab_test_id=ab_test_id,
        experiment_id=experiment_id,
        customer_id=customer_id,
        subject="Participate in Our A/B Test"
    )

    return {"message": "Email sent successfully to the customer."}

@app.get("/track/click/{ab_test_id}/{experiment_id}/{customer_id}")
async def track_click(
    ab_test_id: int,
    experiment_id: int,
    customer_id: int,
    db: Session = Depends(get_db)  
):
    """
    Track a click event for a specific customer in an A/B test.

    This endpoint is triggered when the customer clicks on a link in the email. 
    It retrieves the corresponding record from the 'ab_test_results' table and updates 
    the `clicked_link` field to `True`, indicating that the customer has clicked the link.

    **Parameters:**
    - `ab_test_id (int)`: The ID of the A/B test that the customer is participating in.
    - `experiment_id (int)`: The ID of the experiment within the A/B test.
    - `customer_id (int)`: The ID of the customer who clicked the link.
    - `db (Session)`: The database session provided by FastAPI's dependency injection system.

    **Returns:**
    - A message confirming that the click was tracked successfully.

    **Raises:**
    - `HTTPException`: If no record is found in the `ab_test_results` table for the provided IDs, a 404 error will be raised.
    """
    click_record = db.query(models1.AbTestResults).filter(
        models1.AbTestResults.ab_test_id == ab_test_id,
        models1.AbTestResults.experiment_id == experiment_id,
        models1.AbTestResults.customer_id == customer_id
    ).first()  

    if not click_record:
        raise HTTPException(status_code=404, detail="Test result not found")

    click_record.clicked_link = True
    db.commit() 
    return {"message": "Click tracked successfully"}
