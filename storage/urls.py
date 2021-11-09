'''
    storage module URL Configuration
'''

from django.urls import include, path
from storage.views import (
    FileDownload,
)

urlpatterns = [
    path('url/<int:fid>', FileDownload.as_view(), name='file_upload'),
]
