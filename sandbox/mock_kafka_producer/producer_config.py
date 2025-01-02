import logging, logging.config
import json
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from confluent_kafka.admin import AdminClient
from confluent_kafka import KafkaException


class Config:

    def __init__(self):

        self.__logger = logging.getLogger(__name__)
        # load env with dotenv utility
        load_dotenv()

        # Initialize public class data members
        self.kafka_bootstrap_servers: str = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"       #connect to Kafka Broker Docker Container
        )
        self.commands_topic: str = os.getenv("KAFKA_TOPIC", "kafka_commands")
        self.poll_interval: float = float(os.getenv("KAFKA_POLL_INTERVAL", "1.0"))

        self.check_kafka_connection

    def set_logger(self, logging_file: str = "logging_config.json"):
        # Load logging configuration from external JSON file
        with open(logging_file, "r") as config_file:
            logging_config = json.load(config_file)
            logging.config.dictConfig(logging_config)

        return self.__logger

    def check_env_variable(self, var_name, default_value) -> None:
        set_environmental_value = os.getenv(var_name, default_value)
        if set_environmental_value == default_value:
            self.__logger.info(
                f"Environment variable {var_name} not set from environment. Using default value: {default_value}"
            )

    def check_kafka_connection(self):
        """Verify connection to Kafka broker"""
        try:
            admin_client = AdminClient({'bootstrap.servers': self.kafka_bootstrap_servers})
            # Try to get cluster metadata - this will fail if no connection
            cluster_metadata = admin_client.list_topics(timeout=10)
            self.__logger.info("Successfully connected to Kafka broker")
            return True
        except KafkaException as e:
            self.__logger.error(f"Failed to connect to Kafka broker: {str(e)}")
            raise