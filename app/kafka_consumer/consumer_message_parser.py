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
from consumer_message_processor import message_format

"""
schema built from user parameters
- - - Message format will determine what?

- if message format is json, only keys are needed --> keys and associated data type can be stored in dictionary
    - - - First key will always be message type



"""


# parser to be used by consumer message processor to read, validate message and store message data
class parser:

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
