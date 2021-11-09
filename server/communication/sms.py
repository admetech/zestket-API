'''
Collection of basic SMS functions
'''
# import native libraries
import requests

# Django libraries
from django.conf import settings

# import Local libraries
from server.communication.providers import TwilioService

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# class KaleyraSMSService:
#     '''
#     Generic SMS class designed to use the kaleyra SMS service
#     '''
    
#     SID = settings.SMS['kaleyra']['SID']
#     API_KEY = settings.SMS['kaleyra']['API_KEY']
#     API_DOMAIN = settings.SMS['kaleyra']['API_DOMAIN']
#     SENDER_ID = settings.SMS['kaleyra']['SENDER_ID']
#     TEMPLATE_ID = settings.SMS['kaleyra']['TEMPLATE_ID']

#     SMS_API_ENDPOINT = f"{API_DOMAIN}/{SID}/messages"

#     def send_SMS(self, message, to, sender=None, template_id=None, sms_type=None):
#         '''
#             Sent the Given SMS to the recept
#         '''
#         # Headers
#         headers = {
#             'Content-Type'  : 'application/x-www-form-urlencoded',
#             'api-key'       : self.API_KEY
#         }

#         payload = {
#             'to'            : to,
#             'type'          : sms_type if sms_type is not None else 'default',
#             'sender'        : sender if sender is not None else self.SENDER_ID,
#             'body'          : message,
#             'callback'      : '',
#             'template_id'   : template_id if template_id is not None else self.TEMPLATE_ID,
#         }
#         try:
#             response = requests.post(self.SMS_API_ENDPOINT, data=payload, headers=headers)
#             return response
#         except Exception as e:
#             logger.error(f'KaleyraSMSService.send_SMS : {e}')
#             return str(e)

class TwilioSMSService(TwilioService):
    '''
    Generic SMS class designed to use the twilio SMS service
    '''
    FROM = settings.SMS['twilio']['FROM']
    TEMPLATE_ID = settings.SMS['twilio']['TEMPLATE_ID']

    def send_SMS(self, message, to):
        '''
            Sent the Given SMS to the recept
        '''

        # State variables
        response = None
        status = False
        error = None

        try:
            response = self.CLIENT.messages.create(
                    body = message,
                    from_= self.FROM,
                    to = to,
                )
            
            status = True if response.sid else False
        except Exception as e:
            logger.error(f'TwilioSMSService.send_SMS : {e}')
            error = str(e)

        return {
            'status'    : status,
            'response'  : response.sid,
            'error'     : error,   
        }