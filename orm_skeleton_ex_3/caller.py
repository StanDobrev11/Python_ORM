import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Shoe, Person


# Create queries within functions

def add_shoes():
    shoe = Shoe(
        brand='Nike',
        size=40
    )
    shoe.save()

    shoe = Shoe(
        brand='Nike',
        size=41
    )
    shoe.save()

    shoe = Shoe(
        brand='Adidas',
        size=39
    )
    shoe.save()

    shoe = Shoe(
        brand='Puma',
        size=41
    )
    shoe.save()

    return "Shoes created and saved"

# print(add_shoes())

print(Person.objects.all())