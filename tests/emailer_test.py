import pytest

from app.emailer.emailer import emailer
from app.template_engine.template_engine import TemplateEngine


class TestEmail:
    @pytest.fixture
    def manager(self):
        templater = TemplateEngine()  # initialize template manager to use in email test
        return templater  # pass manager into parameters of the fuctions it needs

    def test_email(self, manager):

        content: str = manager.render_template(
            "email_verification",
            name="John Doe",
            verification_url="http://example.com/verify/1234",
        )
        emailer.send_email("content", content, "recipient")

        # test send a email, .send_email does not return any return code
        # so just send email and pytest will display error more easy to pinpoint.
