import json
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field

from users.permission.permission import PermissionDjangoObjectType
from users.permission.graphql.permission import (
    AllowAuthenticated,
    AllowStaff,
    AllowAny,
)


from users.models import Address

# Geo Location vector convetion to PGSQL type
class GeoJSON(graphene.Scalar):
    @classmethod
    def serialize(cls, value):
        return json.loads(value.geojson)


# these function are important, do not change it
@convert_django_field.register(models.GeometryField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(GeoJSON, description=field.help_text, required=not field.null)


# User Filter class
class UserFilter(django_filters.FilterSet):
    class Meta:
        model = get_user_model()
        fields = {
            "email": ["exact"],
            "name": ["exact"],
        }


# user node
class UserNode(DjangoObjectType):
    """
    User Node for the user object
    """

    class Meta:
        model = get_user_model()
        model_operations = ["create", "update"]
        lookup_field = "username"
        interfaces = (graphene.relay.Node,)
        exclude = [
            "username",
            "password",
            "date_joined",
            "updated_at",
            "is_superuser",
            "is_staff",
            "last_login",
        ]


# User address Filter class
class UserAddressFilter(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = {}


# user address node
class UserAddressNode(PermissionDjangoObjectType):

    """
    User Address Node for the user's address
    """

    permission_classes = (AllowStaff, AllowAuthenticated)

    class Meta:
        model = Address
        model_operations = ["create", "update"]
        interfaces = (graphene.relay.Node,)
        exclude = ["created_at", "created_by", "updated_at", "updated_by"]
