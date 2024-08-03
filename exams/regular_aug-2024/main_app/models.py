from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import CustomAstronautManager
from main_app.validators import phone_number_validator


# Create your models here.
class Astronaut(models.Model):
    objects = CustomAstronautManager()

    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2), ]
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator, ],
        unique=True
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), ]
    )

    updated_at = models.DateTimeField(auto_now=True)


class Spacecraft(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2), ]
    )
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.SmallIntegerField(
        validators=[MinValueValidator(1), ]
    )

    weight = models.FloatField(
        validators=[MinValueValidator(0.0), ]
    )

    launch_date = models.DateField()

    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    MISSION_CHOICES = (
        ("Planned", "Planned"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed")
    )
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2), ]
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=MISSION_CHOICES,
        default="Planned",
    )

    launch_date = models.DateField()

    updated_at = models.DateTimeField(auto_now=True)

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions',
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name="missions",
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commander",
    )
