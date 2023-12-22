import os
from functools import reduce

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


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


def show_unfinished_tasks():
    return '\n'.join(str(task) for task in Task.objects.filter(is_finished=False))


def complete_odd_tasks():
    all_task = Task.objects.all()

    for task in all_task:
        if task.id % 2 == 1:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    result = ''
    for ch in text:
        result += chr(ord(ch) - 3)

    Task.objects.filter(title=task_title).update(description=result)


def populate_rooms(room_number, room_type, capacity, amenities, price_per_night):
    HotelRoom.objects.create(
        room_number=room_number,
        room_type=room_type,
        capacity=capacity,
        amenities=amenities,
        price_per_night=price_per_night,
    )


def get_deluxe_rooms():
    all_rooms = HotelRoom.objects.all()

    result = []
    for room in all_rooms:
        if room.id % 2 == 0:
            result.append(room)

    return '\n'.join(str(room) for room in result)


def increase_room_capacity():
    all_rooms = HotelRoom.objects.all().order_by('id')

    for i, room in enumerate(all_rooms):
        if not room.is_reserved:
            continue
        if i == 0:
            room.capacity += room.id
        else:
            room.capacity += all_rooms[i - 1].capacity

        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved:
        last_room.delete()


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
# print(get_recent_cars())

# populate_rooms(101, 'Standard', 2, 'Tv', 100.00)
# populate_rooms(201, 'Deluxe', 3, 'Wi-Fi', 200.00)
# populate_rooms(501, 'Deluxe', 6, 'Jacuzzi', 400.00)
# increase_room_capacity()
