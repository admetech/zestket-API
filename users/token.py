from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key and some user state that's sure to change
        after a user account is validated to produce a token that invalidated 
        when it's used:
        
        1. is_verified_email state, is changed once the user account is verified.
        
        Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually
        invalidates the token.
        
        Running this data through salted_hmac() prevents token cracking
        attempts using the token, provided the secret isn't compromised.
        """
        return str(user.pk) + str(user.is_verified_email) + str(timestamp) + str(user.password)

class ActivationToken:
    def user_activation_token(self, user):
        '''
        Generate and return the token for the user
        '''
        return AccountActivationTokenGenerator.make_token(AccountActivationTokenGenerator(),user)

    def user_uid(self, user):
        '''
        Generate and return the URL safe id for the user
        '''
        return urlsafe_base64_encode(force_bytes(user.username))

    def validate_token(self, user_details, token):
        '''
        Validate the give user token for the given user
        '''
        return AccountActivationTokenGenerator.check_token(AccountActivationTokenGenerator(), user_details, token)
    
    def validate_user_token(self, uidb64, token):
        '''
        Validate the give token and user username (base64 encoded).
        '''
        username = force_text(urlsafe_base64_decode(uidb64))
        try:
            user_details = get_user_model().objects.get(username=username)
        except Exception as e:
            logger.error(e)
            return False

        try :
            status = AccountActivationTokenGenerator.check_token(AccountActivationTokenGenerator(), user_details, token)
            return status
        except Exception as e:
            logger.error(e)
            return False

class PasswordResetToken:
    '''
        User Password Reset Token
    '''
    def user_password_reset_token(self, user):
        '''
        Generate and return the token for the user
        '''
        return PasswordResetTokenGenerator.make_token(PasswordResetTokenGenerator(),user)

    def user_uid(self, user):
        '''
        Generate and return the URL safe id for the user
        '''
        return urlsafe_base64_encode(force_bytes(user.username))

    def validate_token(self, user_details, token):
        '''
        Validate the give user token for the given user
        '''
        return PasswordResetTokenGenerator.check_token(PasswordResetTokenGenerator(), user_details, token)
    
    def validate_user_token(self, uidb64, token):
        '''
        Validate the give token and user username (base64 encoded).
        '''
        username = force_text(urlsafe_base64_decode(uidb64))
        try:
            user_details = get_user_model().objects.get(username=username)
        except Exception as e:
            logger.error(e)
            return False

        try :
            status = PasswordResetTokenGenerator.check_token(PasswordResetTokenGenerator(), user_details, token)
            return status
        except Exception as e:
            logger.error(e)            
            return False
