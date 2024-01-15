from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models


# Create your models here.
# class FinancialData(models.Model):
#     class Meta:
#         abstract = True
#
#     date = models.DateField(primary_key=True, unique=True)
#     open = models.DecimalField(max_digits=15, decimal_places=3)
#     high = models.DecimalField(max_digits=15, decimal_places=3)
#     low = models.DecimalField(max_digits=15, decimal_places=3)
#     close = models.DecimalField(max_digits=15, decimal_places=3)
#     volume = models.BigIntegerField()
#
#     def clean(self):
#         if not self.open and not self.close:
#             raise ValidationError('Empty data')
#
#
# class BitCoin(FinancialData):
#
#     def save(self, *args, **kwargs):
#         super().clean()
#
#         super().save(*args, **kwargs)

class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(limit_value=2, message="Name must be at least 2 characters long."),
                    validators.MaxLengthValidator(limit_value=100, message="Name cannot exceed 100 characters.")
                    ]
    )
    location = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(limit_value=2, message="Location must be at least 2 characters long."),
            validators.MaxLengthValidator(limit_value=200, message="Location cannot exceed 200 characters.")
        ]
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(limit_value=0, message="Rating must be at least 0.00."),
            validators.MaxLengthValidator(limit_value=5, message="Rating cannot exceed 5.00.")
        ]
    )
