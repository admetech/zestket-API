'''
Collection of basic mailing functions
'''
from django.conf import settings
from django.core.mail import send_mail

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class BaseMails:
    '''
    Generic mails class which send the mail to the user
    '''
    from_host = "noreply@"+settings.HOST_URL

    def send_mail(self, subject, message, to, from_host, html_message):
        '''
            Sent the Given Email to the recept
        '''
        # State variables
        response = None
        status = False
        error = None

        try:
            response = send_mail(
                subject,
                message, 
                from_host, 
                [to],
                html_message=html_message,
                fail_silently=False,
            )
            status = bool(response)
        except Exception as e:
            logger.error(f'BaseMails.send_mail : {e}')
        
        return {
            'status'    : status,
            'response'  : response,
            'error'     : error,   
        }