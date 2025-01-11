import sys
import signal
from app.kafka_consumer.consumer_config import ConsumerConfig
from confluent_kafka import Consumer, KafkaError
from enum import Enum
import logging
import time


class message_format(Enum):
    JSON = "JSON"
    """
    Other possible message formats yet to be discussed/branistormed...
    """


# Define the ConsumerProcessor class to process messages from Kafka producer
"""
Consumer Processor is a wrapper around the Kafka Consumer that subscribes to the commands topic and processes messages.
It initializes the Kafka Consumer with the required settings and subscribes to the commands topic.
The way in which a message is processed will be determined by a variety of methods that will be defined in the class.
"""

"""
Need to store mapping for message types and associated schema/logic
"""


class ConsumerProcessor:
    def __init__(self):

        # Initialize the Config class to load environment variables and set up logging
        settings = ConsumerConfig()
        self.consumer_logger = settings.set_logger_config() #change to *Initialize logger.

        # Check if the required environment variables are set, otherwise log a warning/disclaimer
        settings.check_env_variable("KAFKA_BOOTSTRAP_SERVERS", f"{settings.kafka_bootstrap_servers}")
        settings.check_env_variable("KAFKA_TOPIC", f"{settings.kafka_topic}")
        settings.check_env_variable(f"CONSUMER_GROUP", f"{settings.consumer_group}")
        settings.check_env_variable(f"AUTO_OFFSET_RESET", f"{settings.auto_offset_reset}")

        # Initialize the Kafka Consumer with settings from the `.env` file using Config instance
        settings.check_kafka_connection(settings.kafka_bootstrap_servers)

        try:
            self.consumer = Consumer(
                {
                    "bootstrap.servers": settings.kafka_bootstrap_servers,
                    "group.id": settings.consumer_group,
                    "auto.offset.reset": settings.auto_offset_reset,
                }
            )
            # Subscribe to topic
            
            self.consumer.subscribe([settings.kafka_topic])
            self.consumer_logger.info(
                "Kafka consumer initialized"
            )
        except Exception as init_consumer_error:
            self.consumer_logger.error(
                f"Failed to initialize Kafka consumer: {init_consumer_error}"
            )
            sys.exit(1)

        # Register signal handlers for graceful termination
        signal.signal(signal.SIGINT, self.__signal_handler)
        signal.signal(signal.SIGTERM, self.__signal_handler)

    def __signal_handler(self, signal, frame):
        """Graceful shutdown of the consumer on receiving SIGINT or SIGTERM."""
        self.consumer_logger.info("Shutting down consumer...")
        self.consumer.close()
        sys.exit(0)

    # continuously pull
    def poll_messages(self, polling_interval: float = 1.0, test=False) -> str:
        old_message = None  #create persistent  old message acrosss loop interations , put in if statement?

        while self:  

            message = self.consumer.poll(polling_interval)

            if message is None:
                if test==True:      #return the last message polled if ran in test mode
                    if old_message is not None:
                        return old_message
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    self.consumer_logger.info(
                        f"End of partition reached {message.partition()}"
                    )
                elif message.error():
                    self.consumer_logger.error(
                        f"Error occurred: {message.error().str()}"
                    )
                    break
            else:
                message = message.value().decode("utf-8")
                old_message = message
                """Continuously poll for messages from subscribed topics."""
                try:
                    # Logic to extract message type
                    self.consumer_logger.info(f"Processing Message:{message}")
                # keyboard interrupt will stop consumer polling and cleanup consumer
                except KeyboardInterrupt:
                    self.signal_handler(signal.SIGINT, None)




# main function entry block dev testing execution only--------------
def main():

    consumer_processor = ConsumerProcessor()

    # Start polling for messages
    consumer_processor.poll_messages()


if __name__ == "__main__":
    main()
