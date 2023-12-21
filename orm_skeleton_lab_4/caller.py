import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Student


# Create and check models
def add_students():
    students = [('FC5204', 'John', 'Doe', '1995-05-15', 'john.doe@university.com'),
                ('FE0054', 'Jane', 'Smith', None, 'jane.smith@university.com'),
                ('FH2014', 'Alice', 'Johnson', '1998-02-10', 'alice.johnson@university.com'),
                ('FH2015', 'Bob', 'Wilson', '1996-11-25', 'bob.wilson@university.com')]

    for student_details in students:
        student = Student(*student_details)
        student.save()

    return "Students created"


# Run and print your queries

print(add_students())
print(Student.objects.all())
