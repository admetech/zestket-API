# This is the reference module from the biztyz application
from django.contrib.gis.db import models
from server.db_manager import BiztyzModel

from storage.models import (
    FileStorage
)

class BusinessDetail(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=250)
    logo = models.CharField(max_length=250, blank=True, null=True)
    website = models.CharField(max_length=250, blank=True, null=True)
    gst = models.CharField(db_column='GST', max_length=50, blank=True, null=True)  # Field name made lowercase.
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'business_businessdetail'

class Store(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    branch = models.CharField(max_length=250)
    location = models.CharField(max_length=250, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    coordinate = models.GeometryField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField()
    updated_by = models.IntegerField(blank=True, null=True)
    business = models.ForeignKey(BusinessDetail, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'business_store'
        unique_together = (('business', 'branch'),)

class BusinsessEmployeeRole(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    identifier = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users_userrole'

class BusinsessEmployee(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    name = models.CharField(max_length=120, blank=True, null=True)
    gender = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=254, blank=True, null=True)
    avatar = models.CharField(max_length=250, blank=True, null=True)
    company = models.ForeignKey(BusinessDetail, models.DO_NOTHING)
    role = models.ForeignKey(BusinsessEmployeeRole, models.DO_NOTHING)
    store = models.ForeignKey(Store, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user'

class ProductBrand(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=256, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=50)
    related_company = models.ForeignKey(BusinessDetail, models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'inventory_productbrand'


class ProductCategory(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=150)
    slug = models.CharField(unique=True, max_length=50)
    parent_category = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'inventory_productcategory'

class BusinessAndProductCategory(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    productcategory = models.ForeignKey(ProductCategory, models.DO_NOTHING)
    company = models.ForeignKey(BusinessDetail, models.DO_NOTHING)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'inventory_businessandproductcategory'

class Product(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    name = models.CharField(max_length=250)
    is_service = models.BooleanField()
    
    sku_code = models.CharField(max_length=50)
    upc_code = models.CharField(max_length=30, blank=True, null=True)
    ian_code = models.CharField(max_length=30, blank=True, null=True)
    mpn_code = models.CharField(max_length=100, blank=True, null=True)
    isbn_code = models.CharField(max_length=30, blank=True, null=True)
    
    is_returnable = models.BooleanField()
    
    brand = models.ForeignKey(ProductBrand, models.DO_NOTHING)
    category = models.ForeignKey(ProductCategory, models.DO_NOTHING)
    
    company = models.ForeignKey(BusinessDetail, models.DO_NOTHING)
    
    hsn_code = models.CharField(max_length=30, blank=True, null=True)
    buy_link = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField()

    pictures = models.ManyToManyField(FileStorage, through='ProductPicturesLog')

    class Meta:
        managed = False
        db_table = 'inventory_product'
        unique_together = (('sku_code', 'company'),)

class ProductPicturesLog(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    picture = models.ForeignKey(FileStorage, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventory_productpictureslog'

class ProductPrice(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    is_live = models.BooleanField()
    sales_price = models.DecimalField(max_digits=18, decimal_places=4)
    cost_price = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    tax_included = models.BooleanField()
    discount_type = models.CharField(max_length=1)
    retail_price = models.DecimalField(max_digits=18, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'inventory_productprice'


class ProductTax(BiztyzModel):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    is_live = models.BooleanField()
    is_taxable = models.BooleanField()
    cgst = models.DecimalField(max_digits=7, decimal_places=4)
    sgst = models.DecimalField(max_digits=7, decimal_places=4)
    igst = models.DecimalField(max_digits=7, decimal_places=4)
    product = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventory_producttax'