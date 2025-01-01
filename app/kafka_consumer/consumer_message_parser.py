import json
import base64
from typing import Any
from consumer_message_processor import message_format


# parser class will parse message and return data in parsed message
# parser to be used by consumer message processor to read, validate message and store message data
class Parser:

    '''
    - parser constructor will use message type to pull associated data (schema,message format)
    - at the point where the parser is intialized, message type mappings and user paramaters will be stored in application cache ...
    - constructor will only need message type to be able to retrieve expected message schema and parser rules ...
    '''
    def __init__(self, message_type):
        pass
    
    #private method that checks if message aligns with schema of corresponding message type
    def __isvalid_message(self) -> bool:
        pass

    #successfully parsed message will return dictionary of attribute names and their values
    def parse (self) -> dict:
        pass
