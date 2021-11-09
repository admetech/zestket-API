# Permission Manager for the users (Non GraphQL Based)

# import the logging library
import logging

from typing import Any, Optional

from rest_framework.request import Request
from graphql.execution.base import ResolveInfo

from graphene_django import DjangoObjectType
from users.permission.graphql.permission import (
    AllowSuperuser,
    AllowStaff,
    AllowAuthenticated,
    AllowAny,
)

logger = logging.getLogger(__name__)


class UserPermission:
    def hasPermission(self, request, permissions) -> bool:
        if isinstance(request, Request):
            return bool(
                list(
                    filter(
                        lambda permission: getattr(permission, "has_permission")(
                            permission, request, None
                        ),
                        permissions,
                    )
                )
            )
        elif isinstance(request, ResolveInfo):
            return bool(
                list(
                    filter(
                        lambda permission: getattr(permission, "has_permission")(
                            request
                        ),
                        permissions,
                    )
                )
            )
        return False

    def doesNotHasPermission(self, request, permissions) -> bool:
        if isinstance(request, Request):
            return not getattr(permission, "has_permission")(permission, request, None)
        elif isinstance(request, ResolveInfo):
            return not getattr(permission, "has_permission")(request)
        return False


# additional filter override for the qeryset
class PermissionDjangoObjectType(DjangoObjectType):
    """
    A permission class based DjangoObjectType override
    """

    # these user is allowed all data
    permission_classes = (
        AllowSuperuser,
        AllowStaff,
    )  # keep the , at the end to keep it ittratable

    # only data that is created by them
    self_data_permission = (AllowSuperuser,)

    class Meta:
        abstract = True

    """
        Override the get_node with permission
    """

    @classmethod
    def get_node(cls, info, id):
        queryset = cls.get_queryset(cls._meta.model.objects, info)
        try:
            if bool(
                list(
                    filter(
                        lambda perm: perm.has_node_permission(info=info, id=id),
                        cls.permission_classes,
                    )
                )
            ):
                return queryset.filter(customer=info.context.user).get(id=id)
            return queryset.none()
        except cls._meta.model.DoesNotExist:
            return None

    """
        Override get_queryset with permission
    """

    @classmethod
    def get_queryset(cls, queryset, info):
        """Roles based data filtering"""
        # if the given user role is defined in the permission_classes then return the data
        if bool(
            list(
                filter(
                    lambda perm: perm.has_filter_permission(info),
                    cls.permission_classes,
                )
            )
        ):
            return queryset.filter(customer=info.context.user)

        elif bool(
            list(
                filter(
                    lambda perm: perm.has_filter_permission(info),
                    cls.self_data_permission,
                )
            )
        ):
            return queryset.filter(customer=info.context.user)

        # return empty data
        return queryset.none()
