import os

import django
from django.db.models import Q, Count

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


def get_top_publisher():
    """It retrieves the author with the greatest number of published articles."""

    top_author = Author.objects.get_authors_by_article_count().first()

    if not top_author or top_author.articles_num < 1:
        return ''

    return f"Top Author: {top_author.full_name} with {top_author.articles_num} published articles."


def get_top_reviewer():
    """
    It retrieves the author with the greatest number of published reviews.
    """

    top_author = Author.objects.annotate(published_reviews=Count('review')).order_by('-published_reviews', 'email').first()

    if not top_author or top_author.published_reviews < 1:
        return ''

    return f"Top Reviewer: {top_author.full_name} with {top_author.published_reviews} published reviews."


# print(get_authors(search_email='@'))
# print(get_top_publisher())
# print(get_top_reviewer())
