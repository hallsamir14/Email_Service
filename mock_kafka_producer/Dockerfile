# Use an official Python runtime as a parent image
FROM python:3.12.2-bullseye

# Set the working directory in the container
WORKDIR /mock_kafkaProducer

# Copy the contents of local 'mock_kafkaProducer/' directory into the current directory of container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot when the container launches
CMD ["python", "producer.py"]
