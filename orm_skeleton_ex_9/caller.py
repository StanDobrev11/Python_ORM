import os
from datetime import date

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
#
# # Import your models
from main_app.models import RealEstateListing, VideoGame, Invoice, BillingInfo, Programmer, Project, Technology, Task, \
    Exercise


# Print the results
long_and_hard_exercises = Exercise.get_long_and_hard_exercises()
print("Long and hard exercises:")
for exercise in long_and_hard_exercises:
    print('- ' + exercise.name)

short_and_easy_exercises = Exercise.get_short_and_easy_exercises()
print("Short and easy exercises:")
for exercise in short_and_easy_exercises:
    print('- ' + exercise.name)

exercises_within_duration = Exercise.get_exercises_within_duration(20, 40)
print(f"Exercises within 20 - 40 minutes:")
for exercise in exercises_within_duration:
    print('- ' + exercise.name)

exercises_with_difficulty_and_repetitions = Exercise.get_exercises_with_difficulty_and_repetitions(6, 15)
print(f"Exercises with difficulty 6+ and repetitions 15+:")
for exercise in exercises_with_difficulty_and_repetitions:
    print('- ' + exercise.name)
