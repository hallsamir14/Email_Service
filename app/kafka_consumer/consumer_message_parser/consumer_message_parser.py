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
