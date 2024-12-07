# main.py
import os
import sys

"""
from app import App    

if __name__ == "__main__":
    app = App().start()  # Instantiate an instance of App
"""
# dyanmically determine the root path of the project
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import emailer and TemplateMManger objects
from app.emailer import emailer
from app.template_engine.template_engine import TemplateEngine

if __name__ == "__main__":
    """
    In this code, we first create an instance of the `emailer` class (`emailer_instance`),
    and then call the `send_email` method on this instance.
    """
    TemplateManager = TemplateEngine()

    content: str = TemplateManager.render_template(
        "email_verification",
        name="John Doe",
        verification_url="http://example.com/verify/1234",
    )
    emailer.send_email("content", content, "recipient")
