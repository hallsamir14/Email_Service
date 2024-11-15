docker build --network=host -t mock_kafka-producer .

docker run -p 9092:9092 -d mock_kafka-producer