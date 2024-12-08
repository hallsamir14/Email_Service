from builtins import Exception, int, str
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import sys
import os

# dyanmically determine the root path of the project
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# import SMTP_connection object
from app.smtp_api.smtp_connection import smtp_Settings

"""
Emailer class is not necessary as send_email can be used as a stand alone function,
but is used for readability and associated utility
"""


# emailer object will be used as the engine to send emails
class emailer:

    @staticmethod
    def send_email(subject: str, html_content: str, recipient: str):
        settings = smtp_Settings()
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.username
            message["To"] = recipient
            message.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(settings.server, settings.port) as server:
                server.starttls()  # Use TLS
                server.login(settings.username, settings.password)
                server.sendmail(settings.username, recipient, message.as_string())
            logging.info(f"Email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise
