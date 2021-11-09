import json

# django libraries
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.db.models import Q

# graphene libraries
import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field

# local libraries
from biztyz.models import (
    BusinessDetail,
    BusinsessEmployee,
    Store,
    ProductBrand,
    ProductCategory,
    BusinessAndProductCategory,
    Product,
    ProductPicturesLog,
    ProductPrice,
    ProductTax,
)

from storage.schema.node import (
    FileNode,
    ImageNode
)

# import the logging library
import logging

logger = logging.getLogger(__name__)

# BusinsessEmployee node
class BusinessEmployeeNode(DjangoObjectType):
    '''
    BusinsessEmployee Node for the BusinsessEmployee object
    '''

    class Meta:
        model = BusinsessEmployee
        interfaces = (graphene.relay.Node, )
        exclude = []

# BusinsessDetails Filter class
class BusinessDetailFilter(django_filters.FilterSet):
    
    class Meta:
        model = BusinessDetail
        fields = {
            'name': ['exact', 'contains'],
        }

# BusinessDetail node
class BusinessDetailNode(DjangoObjectType):
    '''
    BusinessDetail Node for the BusinessDetail object
    '''

    class Meta:
        model = BusinessDetail
        interfaces = (graphene.relay.Node, )
        exclude = []

    owner = graphene.Field(BusinessEmployeeNode)

    def resolve_owner(self, info):
        return BusinsessEmployee.objects.filter(company=self, role__identifier='OWNER').first()

# ProductBrand Filter class
class ProductBrandFilter(django_filters.FilterSet):
    
    class Meta:
        model = ProductBrand
        fields = {
            'name': ['exact', 'contains'],
        }

# ProductBrand node
class ProductBrandNode(DjangoObjectType):
    '''
    ProductBrand Node for the ProductBrand object
    '''

    class Meta:
        model = ProductBrand
        interfaces = (graphene.relay.Node, )
        exclude = []

# ProductCategory Filter class
class ProductCategoryFilter(django_filters.FilterSet):
    
    class Meta:
        model = ProductCategory
        fields = {
            'name': ['exact', 'contains'],
        }

# ProductCategory node
class ProductCategoryNode(DjangoObjectType):
    '''
    ProductCategory Node for the ProductCategory object
    '''
    
    class Meta:
        model = ProductCategory
        interfaces = (graphene.relay.Node, )
        exclude = []

# BusinessAndProductCategory Filter class
class BusinessAndProductCategoryFilter(django_filters.FilterSet):
    
    class Meta:
        model = BusinessAndProductCategory
        fields = {
            # 'company__name': ['exact', 'contains'],
            'company__slug': ['exact', 'contains'],
            # 'productcategory__name': ['exact', 'contains'],
            # 'productcategory__slug': ['exact', 'contains'],
        }

# BusinessAndProductCategory node
class BusinessAndProductCategoryNode(DjangoObjectType):
    '''
    BusinessAndProductCategory Node for the BusinessAndProductCategory object
    '''
    
    class Meta:
        model = BusinessAndProductCategory
        interfaces = (graphene.relay.Node, )
        exclude = ['company', 'created_at', 'updated_at']
    
    product_count = graphene.Int()

    def resolve_product_count(self, info):
        return Product.objects.filter(category=self.productcategory, company=self.company).count()

# ProductPrice node
class ProductPriceNode(DjangoObjectType):
    '''
    ProductPrice Node for the ProductPrice object
    '''

    # not directly queriable
    class Meta:
        model = ProductPrice
        interfaces = (graphene.relay.Node, )
        exclude = ['is_live']
    
    '''
    To get the details of a single Node or Single DB Row
    '''
    def get_node(info, id):
        return ProductPrice.objects.filter(is_live=True).get(id=id)

    '''
    To get the details of a N nodes or to perform a queryset or filter DB Row
    '''
    def get_queryset(queryset, info):
        return queryset.filter(is_live=True)

# ProductTax node
class ProductTaxNode(DjangoObjectType):
    '''
    ProductTax Node for the ProductTax object
    '''

    # not directly queriable

    class Meta:
        model = ProductTax
        interfaces = (graphene.relay.Node, )
        exclude = ['is_live']
    
    '''
    To get the details of a single Node or Single DB Row
    '''
    def get_node(info, id):
        return ProductTax.objects.get(id=id)

        '''
    To get the details of a N nodes or to perform a queryset or filter DB Row
    '''
    def get_queryset(queryset, info):
        return queryset.filter(is_live=True)

# Product Filter class
class ProductFilter(django_filters.FilterSet):
    
    search = django_filters.CharFilter(method='product_search')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains'],
            # 'sku_code' : ['exact'],
            # 'upc_code' : ['exact'],
            # 'ian_code' : ['exact'],
            # 'mpn_code' : ['exact'],
            # 'isbn_code' : ['exact'],
            # 'is_returnable' : ['exact'],
            'brand__name' : ['exact', 'contains'],
            'brand__slug' : ['exact', 'contains'],
            'category__name' : ['exact', 'contains'],
            'category__slug' : ['exact', 'contains'],
        }
    
    def product_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | 
            Q(sku_code__icontains=value) |
            Q(hsn_code__icontains=value) |
            Q(upc_code__icontains=value) |
            Q(ian_code__icontains=value) |
            Q(mpn_code__icontains=value) |
            Q(isbn_code__icontains=value) |
            Q(description__icontains=value) |
            Q(brand__name__icontains=value) |
            Q(category__name__icontains=value)
        )

# Product node
class ProductNode(DjangoObjectType):
    '''
    Product Node for the Product object
    '''
    
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node, )
        exclude = ['company']

    pictures = graphene.List(ImageNode)

    def resolve_pictures(self, info):
        return self.pictures.all()

    price = graphene.Field(ProductPriceNode)

    def resolve_price(self, info):
        try:
            return ProductPrice.objects.filter(is_live=True).get(product=self)
        except Exception as e:
            logger.error(e)
            return None

    tax = graphene.Field(ProductTaxNode)
    
    def resolve_tax(self, info):
        try:
            return ProductTax.objects.filter(is_live=True).get(product=self)
        except Exception as e:
            logger.error(e)
            return None