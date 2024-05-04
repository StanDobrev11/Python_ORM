import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg
from main_app.models import Director, Actor


# Create and run your queries within functions

def get_directors(search_name=None, search_nationality=None):
    """
    It retrieves director objects by partially and case-insensitively matching the given searching criteria for
    full name and/or nationality.
    """

    if search_name is None and search_nationality is None:
        return ''

    if search_name and search_nationality:
        query = Q(full_name__icontains=search_name, nationality__icontains=search_nationality)

    elif search_name:
        query = Q(full_name__icontains=search_name)

    else:
        query = Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    return '\n'.join(f"Director: "
                     f"{d.full_name}, "
                     f"nationality: {d.nationality}, "
                     f"experience: {d.years_of_experience}"
                     for d in directors)


def get_top_director():
    """
    It retrieves the director with the greatest number of movies.
    """

    top_director = Director.objects.get_directors_by_movies_count().first()

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies.count()}." if top_director else ""


def get_top_actor():
    """
    It retrieves the starring actor with the greatest number of movies s/he starred in.
    """
    top_actor = Actor.objects.annotate(movies_count=Count('movies')).order_by('-movies_count', 'full_name').first()

    if not top_actor or not top_actor.movies.exists():
        return ''

    average_rating = top_actor.movies.aggregate(Avg('rating')).get('rating__avg') or 0

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join(movie.title for movie in top_actor.movies.all())}, "
            f"movies average rating: {round(average_rating, 1)}")


# print(Director.objects.get_directors_by_movies_count())
# print(get_directors(search_name=None, search_nationality='bu'))
# print(get_top_director())
print(get_top_actor())
