import json
import logging, logging.config
from dotenv import load_dotenv
import os


# Config class encapsulate parameters for consumer logging and consumer configuration
class ConsumerConfig:

    def __init__(self):

        # initialize logger as private data member
        self.__logger = None

        # Load settings from environment variables or use default values
        load_dotenv()

        self.kafka_bootstrap_servers = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )  # kafka:9092 when consmer is dockerized
        self.kafka_topic = os.getenv("KAFKA_TOPIC", "kafka_commands")
        self.consumer_group = os.getenv("KAFKA_CONSUMER_GROUP", "my_consumer_group")
        self.auto_offset_reset = os.getenv(
            "AUTO_OFFSET_RESET", "earliest"
        )  # Can be set to 'latest' or 'earliest'

    def set_logger_config(self, logging_file: str = "logging_config.json"):
        # Load logging configuration from external JSON file
        with open(logging_file, "r") as config_file:
            logging_config = json.load(config_file)
            logging.config.dictConfig(logging_config)

        self.__logger = logging.getLogger(__name__)
        return self.__logger

    def check_env_variable(self, var_name, default_value) -> None:
        set_environmental_value = os.getenv(var_name, default_value)
        if set_environmental_value == default_value:
            self.__logger.info(
                f"Environment variable {var_name} not set from environment. Using default value: {default_value}"
            )
