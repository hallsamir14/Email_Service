import pytest
import asyncio
from app.kafka_consumer.consumer_message_processor import ConsumerProcessor
from sandbox.mock_kafka_producer.producer import KafkaProducer
import uuid
import time
import json
from confluent_kafka.admin import AdminClient


class TestConsumer:
    @pytest.fixture(scope="session", autouse=True)
    def ensure_kafka(self):
        """Ensure Kafka is running before tests start"""
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                admin_client = AdminClient({        #connect via admin client to ensure connection
                    'bootstrap.servers': 'localhost:9092'  
                })
                admin_client.list_topics(timeout=10)
                return  # Kafka is running
            except Exception as e:
                if attempt == max_retries - 1:
                    pytest.skip(f"Kafka not available after {max_retries} attempts: {e}")
                time.sleep(retry_delay)

    #initilize mock producer and begin send messages
    @pytest.fixture(scope="function")
    def produce(self):
        producer = KafkaProducer()
        args = producer.parse_arguments()
        message = str(uuid.uuid4()) #send unqique identifier as message content
        
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(producer.send_to_kafka(email=args.email, template = args.template ,message_content=message, duration=args.duration)) #send only 1 message (poll time = 1 sec)
        except KeyboardInterrupt:
            producer.logger.info("Producer shutdown requested.")
        finally:
            producer.shutdown()     
        return message          #pass unique identifier to other functions to validate

    
    def test_consumer(self, produce):
        consumer_processor = ConsumerProcessor() #initialize consumer
        uuid = produce
        # Start polling for messages
        message = consumer_processor.poll_messages(test=True) #poll and store last successful message recieved (not None)

        if message:
            msgJson = json.loads(message)       #turn to json to pull 'content' field
            assert msgJson['content'] == uuid   #validate content field(with unique id) with uuid passed as a parameter


    