import sys
import signal
from consumer_config import ConsumerConfig
from confluent_kafka import Consumer, KafkaError
import logging

# Define the ConsumerProcessor class to process messages from Kafka producer
"""
Consumer Processor is a wrapper around the Kafka Consumer that subscribes to the commands topic and processes messages.
It initializes the Kafka Consumer with the required settings and subscribes to the commands topic.
The way in which a message is processed will be determined by a variety of methods that will be defined in the class.
"""


class ConsumerProcessor:
    def __init__(self):

        # Initialize the Config class to load environment variables and set up logging
        settings = ConsumerConfig()
        self.consumer_logger = settings.set_logger_config()

        # Check if the required environment variables are set, otherwise log a warning/disclaimer
        settings.check_env_variable("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        settings.check_env_variable("KAFKA_TOPIC", "kafka_commands")
        settings.check_env_variable("CONSUMER_GROUP", "my_consumer_group")
        settings.check_env_variable("AUTO_OFFSET_RESET", "earliest")

        # Initialize the Kafka Consumer with settings from the `.env` file using Config instance
        try:
            self.consumer = Consumer(
                {
                    "bootstrap.servers": settings.kafka_bootstrap_servers,
                    "group.id": settings.consumer_group,
                    "auto.offset.reset": settings.auto_offset_reset,
                }
            )
            # Subscribe to topic
            self.consumer.subscribe([self.settings.kafka_topic])
            self.consumer_logger.info(
                "Kafka consumer initialized and subscribed to topics."
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

    def poll_messages(self, polling_interval: float = 1.0):
        """Poll messages continuously from the subscribed topics and display them via info log."""
        while self:
            # Instance of polling a message w/ polling interval
            message = self.consumer.poll(polling_interval)
            if message is None:
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
                """Continuously poll for messages from subscribed topics."""
                try:
                    self.consumer_logger.info(f"Processing Message:{message}")
                # keyboard interrupt will stop consumer polling and cleanup consumer
                except KeyboardInterrupt:
                    self.signal_handler(signal.SIGINT, None)

        # TODO think about how to handle the message to be stored on consumer side
        """
        Why do we want to cache messages on the consumer side if the kafka cluster stores messages persistently?
        Would would caching messages allow us to do that we can't do with the kafka cluster?
        
        """

    def store_message(self, message_store_array):
        """Store the decoded message in an array?"""
        pass


# main function entry block dev testing execution only--------------
def main():

    consumer_processor = ConsumerProcessor()

    # Start polling for messages
    consumer_processor.poll_messages()


if __name__ == "__main__":
    main()
