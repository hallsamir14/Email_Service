import uuid
import asyncio
import json
import logging
import logging.config
import argparse
from confluent_kafka import Producer, KafkaError
from sandbox.mock_kafka_producer.producer_config import Config
from datetime import datetime
from pathlib import Path


class KafkaProducer:
    """
    A class to handle Kafka message production with async capabilities.
    
    This class encapsulates the functionality for producing messages to Kafka topics,
    including connection management, message formatting, and delivery tracking.
    """

    def __init__(self):
        """Initialize the KafkaProducer with configuration and logging setup."""
        self.settings = Config()
        self._setup_logging()
        self._initialize_producer()
        
    def _setup_logging(self):
        """Set up logging configuration from JSON file."""
        config_path = Path(__file__).parent / "logging_config.json"
        with open(config_path, "r") as config_file:
            logging_config = json.load(config_file)
            logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(__name__)

    def _initialize_producer(self):
        """Initialize the Kafka producer with configuration settings."""
        self.producer = Producer({
            "bootstrap.servers": self.settings.kafka_bootstrap_servers,
            "acks": "all",
            "retries": 5,
            "retry.backoff.ms": 300,
        })

    def delivery_report(self, err, msg):
        """
        Callback function for message delivery reports.
        
        Args:
            err: Error information if delivery failed
            msg: Message object containing delivery details
        """
        if err:
            self.logger.error(f"Message delivery failed: {err}")
        else:
            self.logger.info(
                f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}"
            )

    async def send_to_kafka(self, email, template, message_content, duration=None):
        """
        Asynchronously send messages to Kafka topic at regular intervals.
        
        Args:
            message_content: The content to be sent to Kafka
        """
        self.settings.check_kafka_connection(self.settings.kafka_bootstrap_servers)
        start_time = asyncio.get_event_loop().time() #get current time before loop starts
        
        while True:

            if duration is not None:        
                if asyncio.get_event_loop().time() - start_time >= duration:
                    self.logger.info(f"Message production stopped after {duration} seconds")        #stop sending after the duration specified (test mode)
                    break

            message = {
                "uuid": str(uuid.uuid4()),
                "email": email,
                "template": template,
                "content": message_content,
                "timestamp": datetime.now().isoformat(),
            }
            message_json = json.dumps(message)
            
            try:
                self.producer.produce(
                    self.settings.commands_topic,
                    message_json,
                    on_delivery=self.delivery_report
                )
                self.producer.poll(self.settings.poll_interval)
            except KafkaError as e:
                self.logger.error(f"Kafka exception occurred: {e}")
                
            self.logger.debug(f"Sent message: {message_json}")
            await asyncio.sleep(1)

    @staticmethod
    def parse_arguments():
        """
        Parse command line arguments for dynamic message input.
        
        Returns:
            argparse.Namespace: Parsed command line arguments
        """
        parser = argparse.ArgumentParser(description="Process messages to Kafka.")
        parser.add_argument(
            "--email",
            nargs="?",
            default="email@gmail.com",
            help="email"
        )
        parser.add_argument(
            "--template",
            nargs="?",
            default="default_template",
            help="template to be used in email"
        )
        parser.add_argument(
            "--message",
            nargs="?",
            default="Hello Kafka! Producer online Here",
            help="Message to send to Kafka (vals to input into template)"
        )
        parser.add_argument(
            "--duration",
            type=int,
            default=1,
            help="Optional duration in seconds to send messages. If not specified, runs indefinitely."
        )

        args, unknown = parser.parse_known_args()
        return args

    def shutdown(self):
        """Clean up resources and ensure all messages are sent before shutting down."""
        self.producer.flush(30)
        self.logger.info("Flushing remaining messages...")


def main():
    producer = KafkaProducer()
    args = producer.parse_arguments()
    
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(producer.send_to_kafka(args.email, args.template, args.message))
    except KeyboardInterrupt:
        producer.logger.info("Producer shutdown requested.")
    finally:
        producer.shutdown()



if __name__ == "__main__":
    main()