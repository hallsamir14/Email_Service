#current set of commands work if kafka prodcer dockerfile is in working directory
docker build --network=host -t mock_kafka-producer .

docker run -p 9092:9092 -d mock_kafka-producer