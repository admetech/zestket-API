import json
import logging
from datetime import datetime, timedelta
from random import randint

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.gis.db import models
from django.contrib.gis.geos import fromstr, Point
from django.db.models import Q

import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

# Permissions
from users.permission.permission import UserPermission
from users.permission.graphql.permission import AllowAuthenticated, AllowStaff, AllowAny

# get Nodes definitions
from users.schema.node import UserNode, UserAddressNode

from users.models import Address

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CreateOrUpdateUserAddress(graphene.relay.ClientIDMutation):
    """
    Create new user address or Update existing user address
    """

    userAddress = graphene.Field(UserAddressNode)

    class Input:
        id = graphene.ID()
        name = graphene.String()
        longitude = graphene.Float()  # 108.660326
        latitude = graphene.Float()  # 108.660326
        address = graphene.String(required=True)
        locality = graphene.String()
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        pincode = graphene.Int(required=True)
        phone = graphene.String(required=True)
        isDefault = graphene.Boolean(default=False)

    def mutate_and_get_payload(root, info, **input):
        if not UserPermission.hasPermission(UserPermission, info, [AllowAuthenticated]):
            raise Exception("Unauthorized")

        user = info.context.user

        # create customer address
        user_address, created = Address.objects.update_or_create(
            id=from_global_id(input.get("id"))[1] if input.get("id") else None,
            defaults={
                "customer": user,
                "name": input.get("name"),
                "longitude": input.get("longitude"),
                "latitude": input.get("latitude"),
                "address": input.get("address"),
                "locality": input.get("locality"),
                "city": input.get("city"),
                "state": input.get("state"),
                "pincode": input.get("pincode"),
                "phone": input.get("phone"),
                "updated_by": user,
                "isDefault": input.get("isDefault")
                if input.get("isDefault")
                else False,
            },
        )
        if created:
            user_address.created_by = user
            user_address.save()

        # return data
        return CreateOrUpdateUserAddress(userAddress=user_address)


class Mutation(graphene.AbstractType):
    create_or_update_user_address = CreateOrUpdateUserAddress.Field()
