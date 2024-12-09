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

#parser to be used by consumer message processor to read, validate and store message data
class parser:
    def __init__(self, schema:dict[str,int]):
        pass

    def validate_message(self):
        pass

    def store_message_data(self, attribute:Any) -> list[Any]:
        pass

    def parse_message(self) -> int:
        pass

