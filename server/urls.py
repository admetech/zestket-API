"""server URL Configuration"""
# get environment variables
from os import environ

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

# GraphQL Schema
from server.schema import schema

# overriding the GraphQL authentication with DRF authentication
from rest_framework import request as rq
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

# doc configurations
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#!important  
class DRFAuthenticateGraphQLView(GraphQLView):
    '''
    This is overriding the GraphQL default view authentication with DRF authentication, this mades the DRF use for the authentication work
    '''
    def parse_body(self, request):
        if isinstance(request, rq.Request):
            return request.data
        return super(DRFAuthenticateGraphQLView, self).parse_body(request)

    '''
    Overriding the View method with DRF views
    '''
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(['GET', 'POST'])(view)
        return view

# doc schema defination
schema_view = get_schema_view(
   openapi.Info(
      title="Advertyzement API",
      default_version='v1',
      description="API Descriptions",
      terms_of_service="https://www.advertyzement.com/policies/terms/",
      contact=openapi.Contact(email="contact@advertyzement.com"),
      license=openapi.License(name="© Copyright 2021, advertyzement.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('v1/storage/', include('storage.urls')),
    path('v1/user/', include('users.urls.v1')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Change graphiql=True to graphiql=False if you do not want to use the GraphiQL API browser
if settings.DEV:
    urlpatterns = [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('graph', csrf_exempt(DRFAuthenticateGraphQLView.as_view(graphiql=True, schema=schema))),
        # login url for graph internal views
        path('accounts/', include('django.contrib.auth.urls')),
    ] + urlpatterns
else:
    urlpatterns = [
        path('graph', csrf_exempt(DRFAuthenticateGraphQLView.as_view(graphiql=False, schema=schema))),
    ] + urlpatterns

if environ['DJANGO_ENV'] == 'local':
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
