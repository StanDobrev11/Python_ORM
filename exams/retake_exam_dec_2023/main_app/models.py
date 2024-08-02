from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import CustomTennisPlayerManager


# Create your models here.
class TennisPlayer(models.Model):
    objects = CustomTennisPlayerManager()

    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(5),
        ]
    )

    birth_date = models.DateField()

    country = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
        ]
    )

    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(300)
        ]
    )

    is_active = models.BooleanField(
        default=True
    )


class Tournament(models.Model):
    SURFACE_CHOICES = (
        ("Not Selected", "Not Selected"),
        ("Clay", "Clay"),
        ("Grass", "Grass"),
        ("Hard Court", "Hard Court")
    )

    name = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            MinLengthValidator(2),
        ]
    )

    location = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
        ]
    )

    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    start_date = models.DateField()

    surface_type = models.CharField(
        max_length=12,
        choices=SURFACE_CHOICES,
        default='Not Selected'
    )


class Match(models.Model):

    class Meta:
        verbose_name_plural = "Matches"

    score = models.CharField(
        max_length=100
    )

    summary = models.TextField(
        validators=[
            MinLengthValidator(5),
        ]
    )

    date_played = models.DateTimeField()

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name='matches'
    )

    players = models.ManyToManyField(
        to=TennisPlayer,
        related_name='matches'
    )

    winner = models.ForeignKey(
        to=TennisPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wins'
    )

    def __str__(self):
        return f'{self.date_played}'