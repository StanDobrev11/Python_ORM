import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Animal, Mammal, Bird, Reptile
# Create and check models
# Run and print your queries
