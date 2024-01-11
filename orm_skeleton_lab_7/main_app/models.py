from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class BooleanChoiceField(models.BooleanField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, 'Available'),
            (False, 'Not Available'),
        )
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return age


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    class SpecChoices(models.TextChoices):
        Mammals = "Mammals"
        Birds = "Birds"
        Reptiles = "Reptiles"
        Others = "Others"

    # SPECS = (
    #     ("Mammals", "Mammals"),
    #     ("Birds", "Birds"),
    #     ("Reptiles", "Reptiles"),
    #     ("Others", "Others")
    # )
    # specialty = models.CharField(max_length=10, choices=SPECS)
    specialty = models.CharField(max_length=10, choices=SpecChoices.choices)
    managed_animals = models.ManyToManyField(to=Animal)

    def clean(self):
        super().clean()

        # lst_choices = [item[0] for item in self.SpecChoices.choices]

        # if self.specialty not in lst_choices:
        if self.specialty not in self.SpecChoices:
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

    def is_available(self):
        return self.availability


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self):
        additional_info = ""

        if hasattr(self, 'mammal'):
            additional_info = f" Its fur color is {self.mammal.fur_color}."
        elif hasattr(self, 'bird'):
            additional_info = f" Its wingspan is {self.bird.wing_span} cm."
        elif hasattr(self, 'reptile'):
            additional_info = f" Its scale type is {self.reptile.scale_type}."

        return (f"Meet {self.name}! It's {self.species} and it's born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'!{additional_info}")

    def is_endangered(self):
        endangered_species = (
            "Cross River Gorilla", "Orangutan", "Green Turtle"
        )

        if self.species in endangered_species:
            return True
        else:
            return False
