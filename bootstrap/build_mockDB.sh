#In case docker compose is not working, we can build the docker image and run the container using the following commands
#Current set of commands work if Dockerfile is in working/current direcotry
docker build --network=host -t my-mysql-container .

docker run -p 3306:3306 -d my-mysql-container