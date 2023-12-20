from django.db import models


# Create your models here.

class Shoe(models.Model):
    char = models.CharField(max_length=25)
    size = models.PositiveIntegerField()
    brand_name = models.CharField(max_length=25, unique=True)