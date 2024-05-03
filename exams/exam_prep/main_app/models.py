from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class AbstractPerson(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )


class AbstractAwardedAndUpdatedMixin(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(auto_now=True)


class Director(AbstractPerson):
    years_of_experience = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.full_name


class Actor(AbstractPerson, AbstractAwardedAndUpdatedMixin):

    def __str__(self):
        return self.full_name


class Movie(AbstractAwardedAndUpdatedMixin):
    GENRE_CHOICES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    )

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True
    )

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        default='Other'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        default=0
    )

    is_classic = models.BooleanField(
        default=False
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movies'
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.DO_NOTHING,
        related_name='movie',
        null=True,
        blank=True
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='movies'
    )

    def __str__(self):
        return self.title
