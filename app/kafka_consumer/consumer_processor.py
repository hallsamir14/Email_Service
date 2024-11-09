import sys
import json
import signal
from consumer_config import Config
from confluent_kafka import Consumer, KafkaError

# Initialize the Config class to load environment variables and set up logging
settings = Config()
logger = settings.set_logger()

# Check if the required environment variables are set, otherwise log a warning/disclaimer
settings.check_env_variable("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
settings.check_env_variable("COMMANDS_TOPIC", "kafka_commands")
settings.check_env_variable("CONSUMER_GROUP", "my_consumer_group")
settings.check_env_variable("AUTO_OFFSET_RESET", "earliest")

# Define the ConsumerProcessor class to process messages from Kafka
'''
Consumer Processor is a wrapper around the Kafka Consumer that subscribes to the commands topic and processes messages.
It initializes the Kafka Consumer with the required settings and subscribes to the commands topic.
The way in which a message is processed will be determined by a variety of methods that will be defined in the class.
'''


class ConsumerProcessor:
    def __init__(self):
        # Initialize the Kafka Consumer with settings from the `.env` file using Config instance
        try:
            self.consumer = Consumer(
                {
                    "bootstrap.servers": settings.kafka_bootstrap_servers,
                    "group.id": settings.consumer_group,
                    "auto.offset.reset": settings.auto_offset_reset,
                }
            )
            # Subscribe to multiple topics
            self.consumer.subscribe([settings.commands_topic])
            logger.info("Kafka consumer initialized and subscribed to topics.")
        except Exception as init_consumer_error:
            logger.error(f"Failed to initialize Kafka consumer: {init_consumer_error}")
            sys.exit(1)

        # Register signal handlers for graceful termination
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def __log_message(self, message):
        """Log the processing of each message."""
        logger.info(f"Processing message: {message}")

    def signal_handler(self, signal, frame):
        """Graceful shutdown of the consumer on receiving SIGINT or SIGTERM."""
        logger.info("Shutting down consumer...")
        self.consumer.close()
        sys.exit(0)
    
    def poll_messages(self, polling_interval: float = 1.0):
        """Poll messages continuously from the subscribed topics and display them via info log."""
        while self:
            #Instance of polling a message w/ polling interval
            message = self.consumer.poll(polling_interval)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"End of partition reached {message.partition()}")
                elif message.error():
                    logger.error(f"Error occurred: {message.error().str()}")
                    break
            else:
                message = message.value().decode('utf-8')       
                """Continuously poll for messages from subscribed topics."""
                try:
                    self.__log_message(message)
                #keyboard interrupt will stop consumer polling and cleanup consumer
                except KeyboardInterrupt:
                    self.signal_handler(signal.SIGINT, None)
    
        #TODO think about how to handle the message to be stored on consumer side
        '''
        Why do we want to cache messages on the consumer side if the kafka cluster stores messages persistently?
        Would would caching messages allow us to do that we can't do with the kafka cluster?
        
        '''
        def store_message(self, message_store_array):
            """Store the decoded message in an array."""
            pass

 
    def calc_elapsed_time(self,):
        """Calculate the elapsed time between the current time and the time the message was sent."""
        pass

        

# Register signal handlers for graceful termination
consumer_processor = ConsumerProcessor()


# Start polling for messages
consumer_processor.poll_messages()
