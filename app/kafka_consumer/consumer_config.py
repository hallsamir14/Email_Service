import json
import logging
import logging.config
from dotenv import load_dotenv
import os


# Config class encapsulate parameters for consumer logging and consumer configuration
class ConsumerConfig:
    # Load settings from environment variables or use default values
    def __init__(self):

        # load env with dotenv utility function
        load_dotenv()

        self.kafka_bootstrap_servers = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )  # kafka:9092 when consmer is dockerized
        self.commands_topic = os.getenv("COMMANDS_TOPIC", "kafka_commands")
        self.consumer_group = os.getenv("CONSUMER_GROUP", "my_consumer_group")
        self.auto_offset_reset = os.getenv(
            "AUTO_OFFSET_RESET", "earliest"
        )  # Can be set to 'latest' or 'earliest'

        # """

    def set_logger(self, logging_file: str = "logging_config.json"):
        # Load logging configuration from external JSON file
        with open(logging_file, "r") as config_file:
            self.logging_config = json.load(config_file)
            logging.config.dictConfig(self.logging_config)

        self.logger = logging.getLogger(__name__)
        return self.logger
        # """

    def check_env_variable(self, var_name, default_value) -> None:
        value = os.getenv(var_name, default_value)
        if value == default_value:
            print(
                f"Environment variable {var_name} not set. Using default value: {default_value}"
            )
            """
            self.logger.info(
                f"Environment variable {var_name} not set. Using default value: {default_value}"
            )
            """
