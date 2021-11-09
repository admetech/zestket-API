from django.contrib.auth import get_user_model

from django.contrib.gis.db import models
from server.db_manager import BiztyzModel

class FileStorage(BiztyzModel):
    '''
    Stored the data and location related to the files uploaded to the buckets
    '''
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_key = models.CharField(max_length=50, unique=True, help_text='MD5 hash of the file')     # unique name for the file after hashing use for identification
    original_meta_data = models.TextField(null=True)
    original_size = models.IntegerField(null=True, help_text='The size, in bytes, of the uploaded file.')
    original_charset = models.CharField(max_length=255, null=True)
    bucket_name = models.CharField(max_length=255, null=True)
    server_reply = models.TextField(null=True)                      # server reply after storing the object
    image_width = models.IntegerField(null=True, help_text='Width if the file is image')
    image_height = models.IntegerField(null=True, help_text='Height if the file is image')
    image_average_color = models.CharField(null=True, max_length=7, help_text='image average color')

    class Meta:
        managed = False
        db_table = 'storage_filestorage'
