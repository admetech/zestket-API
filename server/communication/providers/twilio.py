'''
Twilio Service Base configurations to be used with other services
'''
# Django libraries
from django.conf import settings

# Othere Library
from twilio.rest import Client

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class TwilioService:
    '''
    Abstract class to connect with the Twilio services
    '''
    
    ACCOUNT_SID = settings.SERVICES['twilio']['SID']
    AUTH_TOKEN = settings.SERVICES['twilio']['AUTH_TOKEN']

    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    def __init__(self, account_sid, auth_token):
        """
            override the authentication
        """
        self.CLIENT = Client(account_sid, auth_token)