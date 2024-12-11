'''import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional
from email.mime.application import MIMEApplication
import uuid
from sqlalchemy.orm import Session
import models1  


# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP server
SMTP_PORT = 465  # SSL port for Gmail
SENDER_EMAIL = "satmatharmenia@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "rwmg kzsj nkwu xfzg"  # Your Gmail App Password (not regular password)

def generate_click_token():
    """
    Generate a unique token for click tracking.

    **Returns:**
    - `click_token (str)`: A randomly generated UUID token for tracking clicks.
    """
    return str(uuid.uuid4())  # Generates a random unique UUID


def get_ab_test_text_skeleton(db: Session, ab_test_id: int):
    """
    Fetch the text skeleton for a given A/B test from the database.

    **Parameters:**
    - `db (Session)`: Database session object.
    - `ab_test_id (int)`: The ID of the A/B test.

    **Returns:**
    - `text_skeleton (str)`: The email body template for the specified A/B test.

    **Raises:**
    - `AttributeError`: If the A/B test ID does not exist.
    """
    return db.query(models1.AbTest).filter(models1.AbTest.ab_test_id == ab_test_id).first().text_skeleton


def store_click_token(db: Session, ab_test_id: int, experiment_id: int, customer_id: int, click_token: str):
    """
    Store the click token in the database for tracking purposes.

    **Parameters:**
    - `db (Session)`: Database session object.
    - `ab_test_id (int)`: The ID of the A/B test.
    - `experiment_id (int)`: The ID of the experiment.
    - `customer_id (int)`: The ID of the customer.
    - `click_token (str)`: The unique token for tracking clicks.

    **Behavior:**
    - Updates an existing record or creates a new one if none exists.
    """
    click_record = db.query(models1.AbTestResults).filter(
        models1.AbTestResults.ab_test_id == ab_test_id,
        models1.AbTestResults.experiment_id == experiment_id,
        models1.AbTestResults.customer_id == customer_id
    ).first()

    if click_record:
        # Update the existing record
        click_record.click_token = click_token
        db.commit()
    else:
        # Create a new record if one does not exist
        new_click_record = models1.AbTestResults(
            ab_test_id=ab_test_id,
            experiment_id=experiment_id,
            customer_id=customer_id,
            click_token=click_token,
            clicked_link=False
        )
        db.add(new_click_record)
        db.commit()


def send_email(
    db: Session,
    recipient_email: List[str],
    ab_test_id: int,
    experiment_id: int,
    customer_id: int,
    subject: str = "Subject of your email",
    attachment: Optional[str] = None
):
    """
    Send an email with a dynamically inserted tracking link.

    **Parameters:**
    - `db (Session)`: Database session object.
    - `recipient_email (List[str])`: List of recipient email addresses.
    - `ab_test_id (int)`: The ID of the A/B test.
    - `experiment_id (int)`: The ID of the experiment.
    - `customer_id (int)`: The ID of the customer.
    - `subject (str)`: The email subject line (default: "Subject of your email").
    - `attachment (Optional[str])`: Path to a file to attach to the email (default: None).

    **Behavior:**
    - Inserts a tracking link dynamically into the email body using the A/B test text skeleton.
    - Stores the click token in the database for future tracking.

    **Raises:**
    - `FileNotFoundError`: If the attachment file is not found.
    - `smtplib.SMTPException`: For errors related to email sending.
    """
    # Generate a unique click token for this email
    click_token = generate_click_token()

    # Store the click token in the database
    store_click_token(db, ab_test_id, experiment_id, customer_id, click_token)

    # Fetch the email body (text_skeleton) from the database
    text_skeleton = get_ab_test_text_skeleton(db, ab_test_id)

    # Create the tracking URL
    tracking_url = f"https://yourserver.com/track/click/{ab_test_id}/{experiment_id}/{customer_id}/{click_token}"

    # Replace placeholder in text_skeleton with the tracking URL
    body = text_skeleton.replace("{tracking_link}", tracking_url)

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(recipient_email)
    msg['Subject'] = subject

    # Add the email body with the dynamic link
    msg.attach(MIMEText(body, 'html'))

    # Attach file if provided
    if attachment:
        try:
            with open(attachment, "rb") as file:
                part = MIMEApplication(file.read(), Name="attachment.pdf")
                part['Content-Disposition'] = f'attachment; filename="attachment.pdf"'
                msg.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

    try:
        # Using Gmail's SMTP server with SSL (Port 465)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Use App Password here
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # Send the email
            print(f"Email sent to {', '.join(recipient_email)}")
    
    except Exception as e:
        print(f"Error sending email: {e}")
'''


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import uuid

# Configuration variables (replace with your actual values)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_email_password"

def generate_click_token() -> str:
    """
    Generate a unique token for tracking clicks.
    """
    return str(uuid.uuid4())

def send_email(
    recipient_email: List[str],
    subject: str,
    body: str
):
    """
    Send an email with a dynamically inserted body.

    **Parameters:**
    - `recipient_email (List[str])`: List of recipient email addresses.
    - `subject (str)`: Subject of the email.
    - `body (str)`: The body of the email, including the tracking link.

    **Behavior:**
    - Sends an email using the SMTP server.

    **Raises:**
    - `smtplib.SMTPException`: If there is an error sending the email.
    """
    try:
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(recipient_email)
        msg['Subject'] = subject

        # Add the email body
        msg.attach(MIMEText(body, 'html'))

        # Using Gmail's SMTP server with SSL (Port 465)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Use App Password here
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # Send the email
            print(f"Email sent to {', '.join(recipient_email)}")
    
    except smtplib.SMTPException as e:
        print(f"Error sending email to {', '.join(recipient_email)}: {e}")
        raise
