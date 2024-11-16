import pytest
import smtplib

from app.utils.SMTP_connection import smtp_Settings


class TestSMTP:
    @pytest.fixture
    def settings(self):
        settings = smtp_Settings()  # get smtp settings
        return settings  # pass function as a argument in other test to use

    def test_server_name(self, settings):
        result = bool(
            settings.server and settings.server.strip()
        )  # ensure server name is not empty
        assert result == True

    def test_server_port(self, settings):  # ensure server port is of type int
        result = isinstance(settings.port, int)
        assert result == True

    def test_server_username(self, settings):
        result = bool(
            settings.username and settings.username.strip()
        )  # ensure username is not empty
        assert result == True

    def test_server_password(self, settings):
        result = bool(
            settings.password and settings.password.strip()
        )  # ensure password is not empty
        assert result == True

    def test_smtp_connection(self, settings):  # ensure connection to server is valid
        server = smtplib.SMTP(settings.server, settings.port)
        server.starttls()

        connection = server.noop()[
            0
        ]  # NO OPERATION COMMAND, server will set back set command codes based o status

        assert connection == 250  # code 250 is sent on successful conection
        server.quit()

    def test_login(self, settings):  # ensure valid login credentials
        server = smtplib.SMTP(settings.server, settings.port)
        server.starttls()
        server.login(settings.username, settings.password)

        server.quit()
