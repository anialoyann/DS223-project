import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional  # <-- Import Optional here
from email.mime.application import MIMEApplication

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP server
SMTP_PORT = 465  # SSL port for Gmail
SENDER_EMAIL = "satmatharmenia@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "rwmg kzsj nkwu xfzg"  # Your Gmail App Password (not regular password)

def send_email(
    recipient_email: List[str],
    subject: str = "Subject of your email",
    body: str = "",
    attachment: Optional[str] = None
):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(recipient_email)
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

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
