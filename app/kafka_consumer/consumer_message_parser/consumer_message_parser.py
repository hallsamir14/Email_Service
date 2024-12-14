# consumer message parser class will parse message and return data in parsed message
"""
Params to determine general message structure and format? 
- - - These params will enable message parser to understand how to read the message
    - attributes/attribute defintions
    - delmiters?
    - grammar?
    - where will parser params come from?/how will they be passed?
    - data types?

Parser general methods/operations (draft)
    - store attributes/message data
    - convert attributes to specified type
    - send data somehere (this is why it needs to be stored) to be used by application
    - #TODO - - - Brainstorm more possible operations that parser may need.
    
"""
import json
import base64
from typing import Any


# parser to be used by consumer message processor to read, validate message and store message data
class parser:
    #schema param is used to define structure and validation rules for message

    #schema format is needed along with message format, how to implement logic?
    def __init__(self):
        pass
        
    def set_schema(self, message_format:str = "JSON"):
        pass

    def validate_message(self):
        pass

    #To be used in parse_message method, will 
    def store_message_data(self, attribute: Any) -> list[Any]:
        pass

    def parse_json_message(self) -> int:
        pass


