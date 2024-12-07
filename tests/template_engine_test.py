import pytest

from app.template_engine.template_engine import TemplateEngine

# other template manager test are private so just make sure .render_template runs with no errors


class TestTemplateEngine:
    @pytest.fixture
    def manager(self):
        manager = TemplateEngine()  # initialize template manager to use in email test
        return manager

    def test_render_template(self, manager):
        content: str = manager.render_template(
            "email_verification",
            name="John Doe",
            verification_url="http://example.com/verify/1234",
        )
        assert isinstance(content, str) == True  # ensure content is of type string
