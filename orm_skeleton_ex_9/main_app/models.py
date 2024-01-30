from datetime import timedelta
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q, F

from main_app.managers import RealEstateListingManager, VideoGameManager
from main_app.validators import RangeValidator, rating_validator, year_validator


# Create your models here.


class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    objects = RealEstateListingManager()


class VideoGame(models.Model):
    MIN_RELEASE_YEAR = 1990
    MAX_RELEASE_YEAR = 2023

    MIN_RATE_VALUE = Decimal(0)
    MAX_RATE_VALUE = Decimal(10.0)

    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)

    release_year = models.PositiveIntegerField(
        validators=[
            # using built-in validators
            # MinValueValidator(limit_value=MIN_RELEASE_YEAR, message="The release year must be between 1990 and 2023"),
            # MaxValueValidator(limit_value=MAX_RELEASE_YEAR, message="The release year must be between 1990 and 2023"),

            # using custom class validator
            # RangeValidator(
            #     min_value=MIN_RELEASE_YEAR,
            #     max_value=MAX_RELEASE_YEAR,
            #     message="The release year must be between 1990 and 2023"
            # ),

            # using custom validator as function
            year_validator,
        ],
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            # MinValueValidator(limit_value=MIN_RATE_VALUE, message="The rating must be between 0.0 and 10.0"),
            # MaxValueValidator(limit_value=MAX_RATE_VALUE, message="The rating must be between 0.0 and 10.0"),
            rating_validator,
        ],
    )

    objects = VideoGameManager()

    def __str__(self):
        return self.title


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)

    @classmethod
    def get_invoices_with_prefix(cls, prefix):
        """
        returns all the invoices (in a queryset), starting with the specific prefix in the invoice number
        """

        return cls.objects.select_related('billing_info').filter(invoice_number__startswith=prefix)

    @classmethod
    def get_invoices_sorted_by_number(cls):
        """
        returns all the invoices (in a queryset), sorted by invoice number (ascending)
        """

        return cls.objects.select_related('billing_info').order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number):
        """
        returns the invoice object by a specific invoice number
        """

        # return cls.objects.get(invoice_number=invoice_number)

        # optimized for performance
        return cls.objects.select_related('billing_info').get(invoice_number=invoice_number)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')

    def get_programmers_with_technologies(self):
        """
        returns all programmers and all technologies, related to the project (in a queryset).
        """
        return self.programmers.prefetch_related('projects__technologies_used')


class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers')

    def get_projects_with_technologies(self):
        """
        Returns all projects and all technologies (for each project), related to the programmer (in a queryset).
        """
        return self.projects.prefetch_related('technologies_used')


class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()

    @classmethod
    def completed_mid_priority_tasks(cls):
        return cls.objects.filter(priority='Medium', is_completed=True)

    @classmethod
    def search_tasks(cls, query):
        return cls.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    @classmethod
    def recent_completed_tasks(cls, days):
        query = Q(is_completed=True) & Q(completion_date__gte=F('creation_date') - timedelta(days=days))

        return cls.objects.filter(query)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @classmethod
    def get_long_and_hard_exercises(cls):
        query = Q(difficulty_level__gte=10) & Q(duration_minutes__gt=30)

        return cls.objects.filter(query)

    @classmethod
    def get_short_and_easy_exercises(cls):
        query = Q(difficulty_level__lt=5) & Q(duration_minutes__lt=15)

        return cls.objects.filter(query)

    @classmethod
    def get_exercises_within_duration(cls, min_duration: int, max_duration: int):
        query = Q(duration_minutes__range=[min_duration, max_duration])

        return cls.objects.filter(query)

    @classmethod
    def get_exercises_with_difficulty_and_repetitions(cls, min_difficulty: int, min_repetitions: int):
        query = Q(difficulty_level__gte=min_difficulty) & Q(repetitions__gte=min_repetitions)

        return cls.objects.filter(query)
