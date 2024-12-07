from dotenv import load_dotenv
import os


class smtp_Settings:
    def __init__(self):
        # load environment variables from .env file
        load_dotenv()
        self.server = os.getenv("SMTP_SERVER", "smtp.mailtrap.io")
        self.port = int(os.getenv("SMTP_PORT", 2525))
        self.username = os.getenv("SMTP_USERNAME", "")
        self.password = os.getenv("SMTP_PASSWORD", "")
