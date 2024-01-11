import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Animal, Mammal, Bird, Reptile, ZooKeeper, Veterinarian, ZooDisplayAnimal

# Create and check models
# Run and print your queries
# keep the data from the previous exercise, so you can reuse it

all_animals_info = ZooDisplayAnimal.objects.all()
for a in all_animals_info:
    print(a.display_info())
    print(a.is_endangered())
