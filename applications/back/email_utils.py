import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import uuid

# Configuration variables (replace with your actual values)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "ani.aloyan2003@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "roky gfog rwix fhjv"  # Your Gmail App Password (not regular password)

def generate_click_token() -> str:
    """
    Generate a unique token for click tracking.

    **Returns:**
    - `click_token (str)`: A randomly generated UUID token for tracking clicks.
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
