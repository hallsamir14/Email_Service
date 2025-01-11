# Use an official Python runtime as a parent image
FROM python:3.12.2-bullseye

# Set the working directory in the container
WORKDIR /mock_kafka_producer

# Copy the contents of local 'mock_kafkaProducer/' directory into the current directory of container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Kafka Broker and Topic (if needed)  (may need to use *host.docker.internal:9092* if you want to connect to the Broker docker containter from this docker container)
ENV KAFKA_BROKER=localhost:9092   
ENV KAFKA_TOPIC=kafka_commands

# Run the Kafka producer script when the container launches
CMD ["python", "producer.py"]

# build image 
# docker build -t kafka-producer .

# run docker container
# docker run -e KAFKA_BROKER=localhost:9092 -e KAFKA_TOPIC=kafka_commands kafka-producer


