import os

import django
from django.db.models import Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author


# Create and run your queries within functions
def get_authors(search_name=None, search_email=None):
    """
    It retrieves author objects by partially and case-insensitively matching the given searching criteria for
    full name and/or email.
    """
    if search_name is None and search_email is None:
        return ''

    if search_name and search_email:
        query = Q(full_name__icontains=search_name, email__icontains=search_email)

    elif search_name:
        query = Q(full_name__icontains=search_name)

    else:
        query = Q(email__icontains=search_email)

    authors = Author.objects.all().filter(query).order_by('-full_name')

    return '\n'.join(f"Author: {author.full_name}, "
                     f"email: {author.email}, "
                     f"status: {'Banned' if author.is_banned else 'Not Banned'}"
                     for author in authors)




# print(get_authors(search_email='@'))
