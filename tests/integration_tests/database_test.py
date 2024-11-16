import time
import pytest
import subprocess
import mysql.connector
from mysql.connector import Error
import docker


class TestDatabase:
    @pytest.fixture(scope="module", autouse=True)
    def start_docker_compose(self, pytestconfig):

        docker_compose_file = pytestconfig.getoption(
            "docker_compose_ecommerce"
        )  # get docker compose file, get option retrieves value for command line option
        client = docker.from_env()

        if docker_compose_file:
            containers = (
                client.containers.list()
            )  # teardown all containers before setting up containers
            for container in containers:
                container.stop()
                container.remove()

            print(f"Starting Docker Compose with {docker_compose_file}")
            # For linux  - - - "$docker compose"
            # For Windows - - - "$docker-compose"
            subprocess.run(
                ["docker", "compose", "-f", docker_compose_file, "up", "-d"], check=True
            )

            yield  # yield to test, pause code and run test before finishing

            containers = client.containers.list()  # teardown all containers
            for container in containers:
                container.stop()
                container.remove()

    @pytest.fixture(scope="module")
    def database_connection(self):
        # Wait for MySQL to be ready (increase if needed)
        for i in range(15):  # Try for 10 seconds
            try:
                connection = mysql.connector.connect(
                    user="root", password="", host="localhost", database="ecommerce"
                )

                yield connection  # let other functions use the connection before closing

                connection.close()
                print("Database is ready")
                break
            except Error as e:
                print(f"Waiting for database... {e}")
                time.sleep(2)
        else:
            pytest.fail("Database didn't become ready in time")

    @pytest.fixture(scope="function")
    def db_cursor(self, database_connection):
        cursor = database_connection.cursor(buffered=True)  # get curser
        yield cursor  # yield cursor to other test
        cursor.close()

    def test_database_table_exists(self, db_cursor):
        # db_cursor is injected here too
        db_cursor.execute("SHOW TABLES LIKE 'users'")  # ensure users table exist
        result = db_cursor.fetchone()
        assert result is not None, "Users table does not exist"

    def test_database_values_exist(self, db_cursor):
        # db_cursor is injected here too
        db_cursor.execute(
            "SELECT * FROM users"
        )  # ensure there are values in users table
        result = db_cursor.fetchone()
        assert result is not None, "No data in table"
