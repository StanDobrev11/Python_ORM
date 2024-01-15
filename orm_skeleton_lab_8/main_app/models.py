from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models

from main_app.validators import validate_menu_categories


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
            validators.MaxValueValidator(limit_value=5, message="Rating cannot exceed 5.00.")
        ]
    )


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)


class RestaurantReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[validators.MaxValueValidator(5)])

    class Meta:
        ordering = ['-rating']
        verbose_name = "Restaurant Review"
        verbose_name_plural = "Restaurant Reviews"
        unique_together = ['reviewer_name', 'restaurant']
        abstract = True


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'
        unique_together = ['reviewer_name', 'restaurant']


class MenuReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(to=Menu, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[validators.MaxValueValidator(5)])

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ['reviewer_name', 'menu']
        indexes = [models.Index(fields=['menu'], name="main_app_menu_review_menu_id")]
