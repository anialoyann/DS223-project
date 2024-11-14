from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from back.database1 import*
import back.models1 as models1, back.schema1 as schema1
from back.models1 import*
from back.schema1 import*
# Create database tables
models1.Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Endpoints for Customers
@app.get("/customers/{customer_id}", response_model=schema1.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/", response_model=schema1.Customer)
def create_customer(customer: schema1.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.put("/customers/{customer_id}", response_model=schema1.Customer)
def update_customer(customer_id: int, customer: schema1.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted"}

@app.get("/engagements/{engagement_id}", response_model=schema1.Engagement)
def read_engagement(engagement_id: int, db: Session = Depends(get_db)):
    engagement = db.query(Engagement).filter(Engagement.engagement_id == engagement_id).first()
    if engagement is None:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return engagement

@app.post("/engagements/", response_model=schema1.Engagement)
def create_engagement(engagement: EngagementCreate, db: Session = Depends(get_db)):
    db_engagement = Engagement(**engagement.dict())
    db.add(db_engagement)
    db.commit()
    db.refresh(db_engagement)
    return db_engagement

@app.put("/engagements/{engagement_id}", response_model=schema1.Engagement)
def update_engagement(engagement_id: int, engagement: EngagementUpdate, db: Session = Depends(get_db)):
    db_engagement = db.query(Engagement).filter(Engagement.engagement_id == engagement_id).first()
    if db_engagement is None:
        raise HTTPException(status_code=404, detail="Engagement not found")
    for key, value in engagement.dict().items():
        setattr(db_engagement, key, value)
    db.commit()
    db.refresh(db_engagement)
    return db_engagement

@app.delete("/engagements/{engagement_id}")
def delete_engagement(engagement_id: int, db: Session = Depends(get_db)):
    db_engagement = db.query(Engagement).filter(Engagement.engagement_id == engagement_id).first()
    if db_engagement is None:
        raise HTTPException(status_code=404, detail="Engagement not found")
    db.delete(db_engagement)
    db.commit()
    return {"message": "Engagement deleted"}

from back.models1 import Segment
from back.schema1 import SegmentCreate, SegmentUpdate

@app.get("/segments/{segment_id}", response_model=schema1.Segment)
def read_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = db.query(Segment).filter(Segment.segment_id == segment_id).first()
    if segment is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment

@app.post("/segments/", response_model=schema1.Segment)
def create_segment(segment: SegmentCreate, db: Session = Depends(get_db)):
    db_segment = Segment(**segment.dict())
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment

@app.put("/segments/{segment_id}", response_model=schema1.Segment)
def update_segment(segment_id: int, segment: SegmentUpdate, db: Session = Depends(get_db)):
    db_segment = db.query(Segment).filter(Segment.segment_id == segment_id).first()
    if db_segment is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    for key, value in segment.dict().items():
        setattr(db_segment, key, value)
    db.commit()
    db.refresh(db_segment)
    return db_segment

@app.delete("/segments/{segment_id}")
def delete_segment(segment_id: int, db: Session = Depends(get_db)):
    db_segment = db.query(Segment).filter(Segment.segment_id == segment_id).first()
    if db_segment is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    db.delete(db_segment)
    db.commit()
    return {"message": "Segment deleted"}

@app.get("/customer_segments/{customer_segment_id}", response_model=schema1.CustomerSegment)
def read_customer_segment(customer_segment_id: int, db: Session = Depends(get_db)):
    customer_segment = db.query(CustomerSegment).filter(CustomerSegment.customer_segment_id == customer_segment_id).first()
    if customer_segment is None:
        raise HTTPException(status_code=404, detail="Customer segment not found")
    return customer_segment

@app.post("/customer_segments/", response_model=schema1.CustomerSegment)
def create_customer_segment(customer_segment: CustomerSegmentCreate, db: Session = Depends(get_db)):
    db_customer_segment = CustomerSegment(**customer_segment.dict())
    db.add(db_customer_segment)
    db.commit()
    db.refresh(db_customer_segment)
    return db_customer_segment

@app.put("/customer_segments/{customer_segment_id}", response_model=schema1.CustomerSegment)
def update_customer_segment(customer_segment_id: int, customer_segment: CustomerSegmentUpdate, db: Session = Depends(get_db)):
    db_customer_segment = db.query(CustomerSegment).filter(CustomerSegment.customer_segment_id == customer_segment_id).first()
    if db_customer_segment is None:
        raise HTTPException(status_code=404, detail="Customer segment not found")
    for key, value in customer_segment.dict().items():
        setattr(db_customer_segment, key, value)
    db.commit()
    db.refresh(db_customer_segment)
    return db_customer_segment

@app.delete("/customer_segments/{customer_segment_id}")
def delete_customer_segment(customer_segment_id: int, db: Session = Depends(get_db)):
    db_customer_segment = db.query(CustomerSegment).filter(CustomerSegment.customer_segment_id == customer_segment_id).first()
    if db_customer_segment is None:
        raise HTTPException(status_code=404, detail="Customer segment not found")
    db.delete(db_customer_segment)
    db.commit()
    return {"message": "Customer segment deleted"}

@app.get("/ab_tests/{ab_test_id}", response_model=schema1.ABTest)
def read_ab_test(ab_test_id: int, db: Session = Depends(get_db)):
    ab_test = db.query(ABTest).filter(ABTest.ab_test_id == ab_test_id).first()
    if ab_test is None:
        raise HTTPException(status_code=404, detail="AB Test not found")
    return ab_test

@app.post("/ab_tests/", response_model=schema1.ABTest)
def create_ab_test(ab_test: ABTestCreate, db: Session = Depends(get_db)):
    db_ab_test = ABTest(**ab_test.dict())
    db.add(db_ab_test)
    db.commit()
    db.refresh(db_ab_test)
    return db_ab_test

@app.put("/ab_tests/{ab_test_id}", response_model=schema1.ABTest)
def update_ab_test(ab_test_id: int, ab_test: ABTestUpdate, db: Session = Depends(get_db)):
    db_ab_test = db.query(ABTest).filter(ABTest.ab_test_id == ab_test_id).first()
    if db_ab_test is None:
        raise HTTPException(status_code=404, detail="AB Test not found")
    for key, value in ab_test.dict().items():
        setattr(db_ab_test, key, value)
    db.commit()
    db.refresh(db_ab_test)
    return db_ab_test

@app.delete("/ab_tests/{ab_test_id}")
def delete_ab_test(ab_test_id: int, db: Session = Depends(get_db)):
    db_ab_test = db.query(ABTest).filter(ABTest.ab_test_id == ab_test_id).first()
    if db_ab_test is None:
        raise HTTPException(status_code=404, detail="AB Test not found")
    db.delete(db_ab_test)
    db.commit()
    return {"message": "AB Test deleted"}

@app.get("/test_results/{test_result_id}", response_model=schema1.TestResult)
def read_test_result(test_result_id: int, db: Session = Depends(get_db)):
    test_result = db.query(TestResult).filter(TestResult.test_result_id == test_result_id).first()
    if test_result is None:
        raise HTTPException(status_code=404, detail="Test result not found")
    return test_result

@app.post("/test_results/", response_model=schema1.TestResult)
def create_test_result(test_result: TestResultCreate, db: Session = Depends(get_db)):
    db_test_result = TestResult(**test_result.dict())
    db.add(db_test_result)
    db.commit()
    db.refresh(db_test_result)
    return db_test_result

@app.put("/test_results/{test_result_id}", response_model=schema1.TestResult)
def update_test_result(test_result_id: int, test_result: TestResultUpdate, db: Session = Depends(get_db)):
    db_test_result = db.query(TestResult).filter(TestResult.test_result_id == test_result_id).first()
    if db_test_result is None:
        raise HTTPException(status_code=404, detail="Test result not found")
    for key, value in test_result.dict().items():
        setattr(db_test_result, key, value)
    db.commit()
    db.refresh(db_test_result)
    return db_test_result

@app.delete("/test_results/{test_result_id}")
def delete_test_result(test_result_id: int, db: Session = Depends(get_db)):
    db_test_result = db.query(TestResult).filter(TestResult.test_result_id == test_result_id).first()
    if db_test_result is None:
        raise HTTPException(status_code=404, detail="Test result not found")
    db.delete(db_test_result)
    db.commit()
    return {"message": "Test result deleted"}