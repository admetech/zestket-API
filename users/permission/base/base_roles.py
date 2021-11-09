# django Libraries
from django.contrib.auth import get_user_model

# import the logging library
import logging

logger = logging.getLogger(__name__)

class BaseRoles():
    '''
        Generic base class for the Roles to be used in both REST and GraphQL call to build the permission and roles stack
    '''

    def isSuperUser(self, user):
        '''
            Given user has the Power of super user
        '''
        return user.is_superuser
        