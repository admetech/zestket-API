# Utlities functions

# native libraries
import base64
import json
from datetime import datetime, timedelta, date

# other local libraries
from server.communication.mail import BaseMails
from server.communication.sms import TwilioSMSService # KaleyraSMSService,
from server.communication.whatsapp import TwilioWhatsAppService

# import the logging library
import logging

logger = logging.getLogger(__name__)

class CommunicationUtilites:
    def SendSMS(self, message, phoneNumber):
        """
        Send out the message to the target user
        """
        try:
            # response = KaleyraSMSService.send_SMS(KaleyraSMSService, 
            #     message = message,
            #     to = phoneNumber,
            #     sms_type = 'OTP', 
            # )
            
            response = TwilioSMSService.send_SMS(TwilioSMSService, 
                message = message,
                to = phoneNumber,
            )
            return response
        except Exception as e:
            logger.error(f"Error Sending SMS : {str(e)}")
            return None

    def SendEmail(self, to, subject, message, from_host, html_message):
        """
        Send out the Email to the target user
        """
        try:
            response = BaseMails.send_mail(BaseMails,
                subject=subject,
                message=message,
                to=to,
                from_host = from_host,
                html_message=html_message,
            )
            return response
        except Exception as e:
            logger.error(f"Error Sending Email : {str(e)}")
            return None

    def SendWhatApp(self, message, phoneNumber):
        """
        Send out the WhatApp message to the target User
        """
        try:
            response = TwilioWhatsAppService.send_whatsapp(TwilioWhatsAppService, 
                message = message,
                to = phoneNumber,
            )
            return response
        except Exception as e:
            logger.error(f"Error Sending WhatsApp : {str(e)}")
            return None
