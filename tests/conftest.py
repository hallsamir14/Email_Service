import pytest
import os
import subprocess
import docker


@pytest.fixture(scope="session", autouse=True)     #run for durAtion of test session automatically
def run_docker_compose(pytestconfig):
    
    docker_compose = os.path.join(str(pytestconfig.rootdir), "sandbox","docker-compose.yml") #get dc path

    client = docker.from_env()

    if docker_compose:
        containers = (
            client.containers.list()
        )  # teardown all containers before setting up containers
        for container in containers:
            container.stop()
            container.remove()

        print(f"Starting Docker Compose with {docker_compose}")
        
        subprocess.run(
            ["docker", "compose", "-f", docker_compose, "up", "-d"], check=True
        )

        yield  # yield to test, pause code and run test before finishing

        containers = client.containers.list()  # teardown all containers
        for container in containers:
            container.stop()
            container.remove()

