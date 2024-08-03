import random
from datetime import date
from django.core.management.base import BaseCommand

import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Spacecraft, Mission


def handle():
    # Create Astronauts
    astronauts = [
        Astronaut(
            name="John Doe",
            phone_number="1234567890",
            is_active=True,
            date_of_birth=date(1980, 5, 20),
            spacewalks=3
        ),
        Astronaut(
            name="Jane Smith",
            phone_number="0987654321",
            is_active=True,
            date_of_birth=date(1985, 7, 15),
            spacewalks=5
        )
    ]
    Astronaut.objects.bulk_create(astronauts)

    # Create Spacecraft
    spacecrafts = [
        Spacecraft(
            name="Endeavour",
            manufacturer="NASA",
            capacity=7,
            weight=2000.0,
            launch_date=date(2021, 6, 10)
        ),
        Spacecraft(
            name="Atlantis",
            manufacturer="SpaceX",
            capacity=5,
            weight=1800.0,
            launch_date=date(2022, 4, 25)
        )
    ]
    Spacecraft.objects.bulk_create(spacecrafts)

    # Create Missions
    mission1 = Mission.objects.create(
        name="Mission to Mars",
        description="Exploring the Martian surface.",
        status="Planned",
        launch_date=date(2023, 9, 15),
        spacecraft=Spacecraft.objects.get(name="Endeavour"),
        commander=Astronaut.objects.get(name="John Doe")
    )

    mission2 = Mission.objects.create(
        name="Lunar Mission",
        description="Returning to the Moon.",
        status="Ongoing",
        launch_date=date(2021, 12, 5),
        spacecraft=Spacecraft.objects.get(name="Atlantis"),
        commander=Astronaut.objects.get(name="Jane Smith")
    )

    # Add Astronauts to Missions
    mission1.astronauts.add(
        Astronaut.objects.get(name="John Doe"),
        Astronaut.objects.get(name="Jane Smith")
    )
    mission2.astronauts.add(Astronaut.objects.get(name="Jane Smith"))


if __name__ == '__main__':
    handle()
