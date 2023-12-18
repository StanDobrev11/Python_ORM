from datetime import date

from django.db import models


# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email_address}"


class Department(models.Model):
    LOCATION_CHOICES = [
        ('Sofia', 'Sofia'),
        ('Plovdiv', 'Plovdiv'),
        ('Burgas', 'Burgas'),
        ('Varna', 'Varna'),
    ]

    code = models.CharField(max_length=4, primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField(default=1, verbose_name="Employees Count")
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, blank=True)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.name} - {self.employees_count}"


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    duration_in_days = models.PositiveIntegerField(null=True, verbose_name="Duration in Days")
    estimated_hours = models.FloatField(null=True, verbose_name="Estimated Hours")
    start_date = models.DateField(verbose_name="Start Date", default=date.today)
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
