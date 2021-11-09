'''
Collection of basic whatsapp functions
'''

# Django libraries
from django.conf import settings

# import Local libraries
from server.communication.providers import TwilioService

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class TwilioWhatsAppService(TwilioService):
    '''
    Generic Whatsapp service class designed to use the twilio WhatsApp service
    '''
    
    FROM = settings.WHATSAPP['twilio']['FROM']

    def send_whatsapp(self, message, to):
        '''
            Sent the Given WhatsApp to the recept
        '''

        # State variables
        response = None
        status = False
        error = None

        try:
            response = self.CLIENT.messages.create(
                    body = message,
                    from_= f"whatsapp:{self.FROM}",
                    to = f"whatsapp:{to}",
                )
            
            status = True if response.sid else False
        except Exception as e:
            logger.error(f'TwilioWhatsAppService.send_whatsapp : {e}')
            error = str(e)

        return {
            'status'    : status,
            'response'  : response.sid,
            'error'     : error
        }