import os
from datetime import date, timedelta

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Animal, Mammal, Bird, Reptile, ZooKeeper, Veterinarian, ZooDisplayAnimal

# Create and check models
# Run and print your queries
# keep the data from the previous exercise, so you can reuse it
v1 = Veterinarian.objects.create(first_name="John", last_name="Doe", phone_number="0896625120", license_number="VET123", availability=False)
print(v1._is_reserved())
v2 = Veterinarian.objects.create(first_name="Alice", last_name="Johnson", phone_number="0896529728", license_number="VET789")
print(v2._is_reserved())
