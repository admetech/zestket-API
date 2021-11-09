from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import hashlib
import json
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from storage.processors.image import (
    ProcessImage
)

from storage.models import (
    FileStorage,
)

# Get an instance of a logger
logger = logging.getLogger(__name__)

class S3Storage:
    '''
        Storage class to abstract the storage function accross the multiple service providers
    '''

    # default credentials

    bucket_name = settings.STORAGE['default']['bucket']
    key         = settings.STORAGE['default']['access_key_id']
    secret      = settings.STORAGE['default']['secret_access_key']

    # initilize the class
    def __init__(self, bucket_name=None, key=None, secret=None):
        """
            Establish the connection.
        """
        if bucket_name:
            self.bucket_name = bucket_name
        if key:  
            self.key = key
        if secret:
            self.secret = secret

        self._bucket = None

        self.client = boto3.client(
            's3',
            aws_access_key_id       = self.key,
            aws_secret_access_key   = self.secret,
            config                  = Config(
                signature_version='s3v4',
                region_name='ap-south-1',
                )
        )
    
    def get_object_url(self, object_data=None, object_id=None, object_name=None, expires_in=600):
        '''
        Return the object URL based on the id of the object from the storage table
        '''
        object_details = None
        # get the object from the database
        try:
            if object_data is not None:
                object_details = object_data
            elif object_id is not None:
                object_details = FileStorage.objects.get(id=object_id)
            elif object_name is not None: 
                object_details = FileStorage.objects.get(file_key=object_name)
        except Exception as e:
            error = "No object found" + str(e)
            raise error

        # generate the signed url for the object
        url = self.client.generate_presigned_url('get_object', Params = {'Bucket': object_details.bucket_name, 'Key': object_details.file_key}, ExpiresIn = expires_in)
        
        # return the URL
        return url
