import os
from functools import reduce

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car


# Create queries within functions
def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species
    )

    return f"{name} is a very cute {species}!"


def create_artifact(
        name: str,
        origin: str,
        age: int,
        description: str,
        is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    all_locations = Location.objects.all().order_by("-id")
    return '\n'.join(str(location) for location in all_locations)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def create_location(name, region, population, description, is_capital):
    Location.objects.create(
        name=name,
        region=region,
        population=population,
        description=description,
        is_capital=is_capital,
    )


def populate_cars(model, year, color, price):
    Car.objects.create(
        model=model,
        year=year,
        color=color,
        price=price,
    )


def apply_discount():
    all_cars = Car.objects.all()

    for car in all_cars:
        discount = reduce(lambda x, y: int(x) + int(y), [int(x) for x in str(car.year)])
        car.price_with_discount = car.price - car.price * discount / 100
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


# create_location('Sofia',
#                 'Sofia Region',
#                 1329000,
#                 'The capital of Bulgaria and the largest city in the country',
#                 False)
# create_location('Plovdiv',
#                 'Plovdiv Region',
#                 346942,
#                 'The second-largest city in Bulgaria with a rich historical heritage',
#                 False)
# create_location('Varna',
#                 'Varna Region',
#                 330486,
#                 'A city known for its sea breeze and beautiful beaches on the Black Sea',
#                 False)


# print(show_all_locations())
# print(get_capitals())
# populate_cars('Mercedes C63 AMG', 2019, 'white', 120000.00)
# populate_cars('Audi Q7 S line', 2023, 'black', 183900.00)
# populate_cars('Chevrolet Corvette', 2021, 'dark grey', 199999.00)
# apply_discount()
print(get_recent_cars())
