'''
Telegram services
'''
# Django libraries
from django.conf import settings

# import native libraries
import requests

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class TelegramService:
    '''
    Telegram services class
    '''
    CHAT_ID = settings.SERVICES['telegram']['CHAT_ID']
    BOT_TOKEN = settings.SERVICES['telegram']['BOT_TOKEN']

    def __init__(self, chat_id = settings.SERVICES['telegram']['CHAT_ID']):
        """
            override the chat_id
        """
        self.CHAT_ID = chat_id

    def send_message(self, text = 'Hello from Telegram bot'):
        '''
            send notification to the Telegram Group/channel/user.
            text = Message to sent 
        '''
        # construct Message
        message = {
            'chat_id' : self.CHAT_ID,
            'text'    : text,
        }

        # construct URL
        url = 'https://api.telegram.org/bot'+ self.BOT_TOKEN +'/sendMessage'

        # send the message
        r = requests.get(url = url, params=message)

        # if r.status_code == 429:
            # call for retry sending message
        #     raise self.retry(exc=r.json(), countdown=60, max_retries=20)
        
        # return the result
        return {
            'status': r.status_code,
            'data'  : r.json(),
        }

    def get_messages(self):
        '''
            get the messages sent to the bot
        '''

        # construct URL
        url = 'https://api.telegram.org/bot'+ self.BOT_TOKEN +'/getUpdates'

        # send the message
        r = requests.get(url = url)

        # return the result
        return {
            'status': r.status_code,
            'data'  : r.json(),
        }