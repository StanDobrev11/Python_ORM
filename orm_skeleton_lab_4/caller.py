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


def get_students_info():
    all_student = Student.objects.all()

    record = []
    for student in all_student:
        record.append(
            f"Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}")

    return '\n'.join(record)


def update_students_emails():
    all_students = Student.objects.all()

    for student in all_students:
        username = student.email.split('@')[0]
        email = username + '@' + 'uni-students.com'
        student.email = email
        student.save()


def truncate_students():
    Student.objects.all().delete()

# Run and print your queries
#
# print(add_students())
# print(Student.objects.all())
# update_students_emails()
# print(get_students_info())
# truncate_students()
