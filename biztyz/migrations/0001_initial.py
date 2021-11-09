# Generated by Django 3.2.4 on 2021-07-03 18:15

import django.contrib.gis.db.models.fields
from django.db import connection, migrations, models
import django.utils.timezone

def create_schema(apps, schema_editor):
    with connection.cursor() as cursor:
        # create the schema if not exist
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS mrktyz;")


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_schema),
        migrations.CreateModel(
            name='BusinessAndProductCategory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'inventory_businessandproductcategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BusinessDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('logo', models.CharField(blank=True, max_length=250, null=True)),
                ('website', models.CharField(blank=True, max_length=250, null=True)),
                ('gst', models.CharField(blank=True, db_column='GST', max_length=50, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'business_businessdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BusinsessEmployee',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('gender', models.CharField(blank=True, max_length=120, null=True)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('avatar', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'users_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BusinsessEmployeeRole',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('hidden', models.BooleanField()),
            ],
            options={
                'db_table': 'users_userrole',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('name', models.CharField(max_length=250)),
                ('is_service', models.BooleanField()),
                ('sku_code', models.CharField(max_length=50)),
                ('upc_code', models.CharField(blank=True, max_length=30, null=True)),
                ('ian_code', models.CharField(blank=True, max_length=30, null=True)),
                ('mpn_code', models.CharField(blank=True, max_length=100, null=True)),
                ('isbn_code', models.CharField(blank=True, max_length=30, null=True)),
                ('is_returnable', models.BooleanField()),
                ('hsn_code', models.CharField(blank=True, max_length=30, null=True)),
                ('buy_link', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_available', models.BooleanField()),
            ],
            options={
                'db_table': 'inventory_product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('name', models.CharField(max_length=150)),
                ('url', models.CharField(blank=True, max_length=256, null=True)),
                ('slug', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'inventory_productbrand',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'inventory_productcategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPicturesLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'inventory_productpictureslog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('is_live', models.BooleanField()),
                ('sales_price', models.DecimalField(decimal_places=4, max_digits=18)),
                ('cost_price', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('tax_included', models.BooleanField()),
                ('discount_type', models.CharField(max_length=1)),
                ('retail_price', models.DecimalField(decimal_places=4, max_digits=18)),
            ],
            options={
                'db_table': 'inventory_productprice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductTax',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('is_live', models.BooleanField()),
                ('is_taxable', models.BooleanField()),
                ('cgst', models.DecimalField(decimal_places=4, max_digits=7)),
                ('sgst', models.DecimalField(decimal_places=4, max_digits=7)),
                ('igst', models.DecimalField(decimal_places=4, max_digits=7)),
            ],
            options={
                'db_table': 'inventory_producttax',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('branch', models.CharField(max_length=250)),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('coordinate', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'business_store',
                'managed': False,
            },
        ),
    ]
