import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .node import(
    BusinessDetailFilter, BusinessDetailNode, BusinessDetail,
    ProductBrandFilter, ProductBrandNode,
    ProductCategoryFilter, ProductCategoryNode, ProductCategory,
    BusinessAndProductCategoryFilter, BusinessAndProductCategoryNode,
    ProductFilter, ProductNode, Product
)

class Query(graphene.ObjectType):
    '''
        Get Businsess details data
        This is a node structure
    '''
    # Company = graphene.relay.Node.Field(BusinessDetailNode)
    
    CompanyDetails = graphene.Field(BusinessDetailNode, slug=graphene.String(required=True))
    
    def resolve_CompanyDetails(root, info, **kwargs):
        '''
            Get Company Details based on slug
        '''
        return BusinessDetail.objects.filter(slug=kwargs['slug']).get()
    
    '''
        Get Product data
        This is a node structure
    '''
    ProductBrand = graphene.relay.Node.Field(ProductBrandNode)
    ProductBrands = DjangoFilterConnectionField(ProductBrandNode, filterset_class=ProductBrandFilter)

    '''
        Get Product data
        This is a node structure
    '''
    ProductCategory = graphene.relay.Node.Field(ProductCategoryNode)
    ProductCategories = DjangoFilterConnectionField(ProductCategoryNode, filterset_class=ProductCategoryFilter, company__Slug=graphene.String(required=False))

    # def resolve_ProductCategories(root, info, **kwargs):
    #     queryset = ProductCategory.objects.filter(id__in=[x['category'] for x in Product.objects.filter(company=BusinessDetail.objects.filter(slug=kwargs['company__Slug']).get()).values('category').distinct() ]).all()
    #     return queryset

    '''
        Get BusinessAndProductCategory data
        This is a node structure
    '''
    BusinessAndProductCategory = graphene.relay.Node.Field(BusinessAndProductCategoryNode)
    BusinessAndProductCategories = DjangoFilterConnectionField(BusinessAndProductCategoryNode, filterset_class=BusinessAndProductCategoryFilter)

    '''
        Get Product data
        This is a node structure
    '''
    Product = graphene.relay.Node.Field(ProductNode)
    Products = DjangoFilterConnectionField(ProductNode, filterset_class=ProductFilter, company__Slug=graphene.String(required=True)) 

    def resolve_Products(root, info, **kwargs):
        return Product.objects.filter(company__slug=kwargs['company__Slug'])