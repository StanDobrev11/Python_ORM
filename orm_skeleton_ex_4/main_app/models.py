from django.db import models


# Custom manager -> usually separate file
class CustomManager(models.Manager):
    def custom_query_filter(self):
        return "Very complex logic here"

# Class using custom manager
class MyModel(models.Model):
    field1 = models.CharField()

    custom_manager = CustomManager()

# Create your models here.
