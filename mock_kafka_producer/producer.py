"""
This script acts as a Kafka producer, designed to run in a microservice architecture where it interacts with Discord.
It takes messages from command-line input or default messages, encodes them into JSON format, and sends them to a Kafka topic.
The script uses asynchronous programming to handle message sending continuously.

Features:
- Configurable Kafka settings using environment variables and a .env file.
- Robust Kafka connection settings including acknowledgments and retries.
- Dynamic message content through command-line arguments.
- Continuous asynchronous message production with controlled polling to manage Kafka message buffer.
- Graceful shutdown handling to ensure all messages are flushed before termination.

Usage:
- This script is typically deployed as part of a larger system where Discord bots collect messages,
  and this producer handles sending those messages to Kafka for further processing or storage.
- It can be customized to handle various data inputs and integrate with different Kafka topics as required by the system architecture.

Dependencies:
- confluent_kafka: Provides Kafka client functionality.
- pydantic_settings: Manages environment-based settings.
- asyncio: For asynchronous operations.
- argparse: For parsing command-line options.
"""

import uuid
import asyncio
import json
import logging
import logging.config
from confluent_kafka import Producer, KafkaError
from pydantic_settings import BaseSettings
from datetime import datetime
import argparse


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "localhost:9092"  # Kafka server address
    commands_topic: str = "kafka_commands"  # Kafka topic to publish messages
    poll_interval: float = 0.1  # Polling interval in seconds for Kafka producer

    class Config:
        env_file = ".env"  # Configuration file for environment variables
        env_file_encoding = "utf-8"


settings = Settings()

# Load logging configuration from a JSON file to setup structured logging
with open("logging_config.json", "r") as config_file:
    logging_config = json.load(config_file)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

# Initialize Kafka Producer with server and retry configurations
producer = Producer(
    {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "acks": "all",  # Ensure all replicas acknowledge the message
        "retries": 5,  # Retry up to 5 times
        "retry.backoff.ms": 300,  # Wait 300ms between retries
    }
)


def delivery_report(err, msg):
    """Callback function for message delivery reports."""
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(
            f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}"
        )


async def send_to_kafka(message_content):
    """Asynchronously sends messages to Kafka topic at regular intervals."""
    while True:
        message = {
            "uuid": str(uuid.uuid4()),
            "content": message_content,
            "timestamp": datetime.now().isoformat(),
        }
        message_json = json.dumps(message)
        try:
            producer.produce(
                settings.commands_topic, message_json, on_delivery=delivery_report
            )
            producer.poll(settings.poll_interval)
        except KafkaError as e:
            logger.error(f"Kafka exception occurred: {e}")
        logger.debug(f"Sent message: {message_json}")
        await asyncio.sleep(1)  # Wait before sending the next message


def parse_arguments():
    """Parse command line arguments for dynamic message input."""
    parser = argparse.ArgumentParser(description="Process messages to Kafka.")
    parser.add_argument(
        "message",
        nargs="?",
        default="Hello Kafka! Producer online Here",
        help="Message to send to Kafka",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_to_kafka(args.message))
    except KeyboardInterrupt:
        logger.info("Producer shutdown requested.")
    finally:
        producer.flush(30)  # Ensure all messages are sent before shutting down
        logger.info("Flushing remaining messages...")
