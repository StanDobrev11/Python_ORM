import os

import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article


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

    top_author = Author.objects.annotate(published_reviews=Count('review')).order_by('-published_reviews',
                                                                                     'email').first()

    if not top_author or top_author.published_reviews < 1:
        return ''

    return f"Top Reviewer: {top_author.full_name} with {top_author.published_reviews} published reviews."


def get_latest_article():
    """
    It retrieves the last published article and returns a string
    """
    last_article = Article.objects.annotate(average_rating=Avg('reviews__rating')).order_by('-published_on').first()

    if last_article is None:
        return ''

    return (f"The latest article is: "
            f"{last_article.title}. "
            f"Authors: {', '.join(author.full_name for author in last_article.authors.all().order_by('full_name'))}. "
            f"Reviewed: {last_article.reviews.count()} times. "
            f"Average Rating: {round(last_article.average_rating, 2) if last_article.average_rating else 0 :.2f}.")


def get_top_rated_article():
    """It retrieves the top-rated article by considering the ratings of published reviews.
    If you happen to have articles with the same top rating results, order them by title,
    ascending, and get the first one.
    """

    top_article = (
        Article.objects
        .annotate(average_rating=Avg('reviews__rating'), reviews_count=Count('reviews'))
        .order_by('-average_rating')
        .first()
    )

    if not top_article or top_article.reviews_count == 0:
        return ''

    return (f"The top-rated article is: {top_article.title}, "
            f"with an average rating of {round(top_article.average_rating, 2) :.2f}, "
            f"reviewed {top_article.reviews_count} times.")


def ban_author(email=None):
    """It retrieves the author object with the given email (exact match) and changes his/her status
    to "Banned" (is_banned=True)."""

    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
    except ObjectDoesNotExist:
        return "No authors banned."

    reviews_count = author.reviews.count()

    author.is_banned = True
    author.reviews.all().delete()
    author.save()

    return f"Author: {author.full_name} is banned! {reviews_count} reviews deleted."

# print(get_authors(search_email='@'))
# print(get_top_publisher())
# print(get_top_reviewer())
# print(get_latest_article())
print(get_top_rated_article())
# print(ban_author('tarnauduc1@t.co'))
