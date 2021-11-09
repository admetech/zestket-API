'''
Collection of mailing functions with their templates
'''

from django.conf import settings
from django.core.mail import send_mail

from django.template.loader import render_to_string

from server.mail import BaseMails

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Mails(BaseMails):
    '''
        User related Mails section
    '''
    def user_activation_token(self, to, activation_url):
        '''
            Sends the User Activation Link to the given Mail address
        '''
        return send_mail(
                "Activation Mail", 
                "activation URL : " + activation_url, 
                self.from_host, 
                [to], 
                fail_silently=False
            )
    
    def user_welcome_mail(self, to, name):
        '''
            Sends the User Welcome Mail
        '''
        # create context
        d = {"name": name}
        
        # load email templates
        text_content = render_to_string('email/welcome_email.txt',d)
        html_content = render_to_string('email/welcome_email.html',d)
        
        return self.send_mail(
                "Thank your brand for building tyz!",
                text_content,
                [to],
                html_message=html_content,
            )

    def user_password_reset_token(self, to, password_reset_url):
        '''
            Sends the User Password Link to the given Mail address
        '''
        return send_mail(
                "Password Reset Mail", 
                "password reset URL : " + password_reset_url, 
                self.from_host, 
                [to], 
                fail_silently=False
            )