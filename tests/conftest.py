import os


# place all parser.addoptions in this file
# centralized location to place docker file paths to be used in integration test
# docker_compose_file = pytestconfig.getoption("docker_file_option_specified_here")
def pytest_addoption(parser):
    conftest_dir = os.path.dirname(os.path.abspath(__file__))
    # get current directory

    # Navigate to the current, then into the 'tests' folder
    # grab the path to the docker compose for the eccommerce sql db
    ecommerce_docker_compose_file = os.path.join(
        conftest_dir, "integration_tests", "test-docker-compose-ecommerce.yml"
    )

    parser.addoption(
        "--docker-compose-ecommerce",
        action="store",
        default=ecommerce_docker_compose_file,
        help="test-docker-compose-ecommerce.yml",
    )
    # add docker file path as a command line option
    # pytest converts - to _
