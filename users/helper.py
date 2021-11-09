'''
Collection of common helper functions
'''
from django.conf import settings

from users.mail import Mails
from users.token import (
    AccountActivationTokenGenerator, ActivationToken,
    PasswordResetToken, PasswordResetTokenGenerator
)

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UserHelper:
    '''
    Helper function for the users
    '''
    def send_activation_mail(self, user):
        '''
            Generates and sends the User Activation Mail
        '''
        # generate the verification token for the user verification
        uid = ActivationToken.user_uid(ActivationToken(),user)
        activation_token = ActivationToken.user_activation_token(ActivationToken(),user)
        activation_url = str(settings.HOST_URL) + "/activate_account/" + str(uid) + "/" + str(activation_token)
        
        # send activation mail
        return Mails.user_activation_token(
            Mails(),
            user.email,
            activation_url,
        )

    def send_password_reset_mail(self, user):
        '''
            Generates and sends the User Password Reset Mail
        '''
        # generate the password reset token for the user password reset
        uid = PasswordResetToken.user_uid(PasswordResetToken(),user)
        password_reset_token = PasswordResetToken.user_password_reset_token(PasswordResetToken(),user)
        password_reset_url = str(settings.HOST_URL) + "/password_reset/" + str(uid) + "/" + str(password_reset_token)
        
        # send activation mail
        return Mails.user_password_reset_token(
            Mails(),
            user.email,
            password_reset_url,
        )