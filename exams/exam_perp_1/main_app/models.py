from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import CustomProfileManager


# Create your models here.
class Profile(models.Model):
    objects = CustomProfileManager()

    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(limit_value=2)]
    )
    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
        help_text='This field is typically a string to accommodate various phone number formats.'
    )

    address = models.TextField(
        help_text='This field can store longer text, suitable for addresses.'
    )

    is_active = models.BooleanField(default=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0.01)]
    )

    in_stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    is_available = models.BooleanField(default=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Order(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='orders')

    products = models.ManyToManyField(to=Product, related_name='orders')

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0.01)]
    )

    creation_date = models.DateTimeField(auto_now_add=True)

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile} - {self.creation_date}"