from django.contrib.gis.db import models

# biztyz db manager
class BiztyzDBManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().using('biztyz_db')
        return qs

# biztyz Models abstract class 
class BiztyzModel(models.Model):
    objects = BiztyzDBManager()

    class Meta:
        abstract = True