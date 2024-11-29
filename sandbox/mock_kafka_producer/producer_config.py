import logging, logging.config
import json
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config:

    def __init__(self):
        # load env with dotenv utility
        load_dotenv()

        # Initialize public class data members
        self.kafka_bootstrap_servers: str = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )
        self.commands_topic: str = os.getenv("KAFKA_TOPIC", "kafka_commands")
        self.poll_interval: float = float(os.getenv("KAFKA_POLL_INTERVAL", "1.0"))

    def set_logger(self, logging_file: str = "logging_config.json"):
        # Load logging configuration from external JSON file
        with open(logging_file, "r") as config_file:
            logging_config = json.load(config_file)
            logging.config.dictConfig(logging_config)

        self.__logger = logging.getLogger(__name__)
        return self.__logger
