# Generated by Django 3.2.4 on 2021-06-06 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FileTransactionLogs',
        ),
        migrations.AlterModelTable(
            name='filestorage',
            table='storage_filestorage',
        ),
    ]
