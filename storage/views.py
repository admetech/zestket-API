from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from storage.processors.storage import S3Storage
        
class FileDownload(APIView):
    '''
    Download the file from the server based on the fid which is provided
    '''
    def get(self, request, fid):
        storage = S3Storage()
        url = storage.get_object_url(object_id=fid)
        return Response({"file": 'ok', 'url':url}, status=200)
