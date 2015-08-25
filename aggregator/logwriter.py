import logging
import logging.handlers
import traceback
from kitchen.text.converters import to_bytes
class logWriter():
    def __init__(self,identifier):
        LOG_FILENAME = 'logs/{}.out'.format(identifier)

        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger(identifier)
        self.my_logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        self.handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, maxBytes=2000, backupCount=0)

        self.my_logger.addHandler(self.handler)

    def write(self,*message):
        try:
            message=' '.join(map(to_bytes,message))
        except:
            message=traceback.format_exc()

        self.my_logger.debug(message)
        

# # Log some messages
# for i in range(20):