import os
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg
from main_app.models import Director, Actor, Movie


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
    top_actor = Actor.objects.annotate(movie_count=Count('movie')).order_by('-movie_count', 'full_name').first()

    if not top_actor or not top_actor.movie.exists():
        return ''

    average_rating = top_actor.movie.aggregate(Avg('rating')).get('rating__avg') or 0

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join(movie.title for movie in top_actor.movie.all())}, "
            f"movies average rating: {round(average_rating, 1)}")


def get_actors_by_movies_count():
    """
    It retrieves the top three actors from all movies, ordered by the number of times the actor has
    participated in movies, descending, then ascending by the actor’s full name.
    """
    actors = Actor.objects.annotate(movies_count=Count('movies')).order_by('-movies_count', 'full_name').all()[:3]

    return '\n'.join(f"{actor.full_name}, participated in {actor.movies_count} movies" for actor in actors)


def get_top_rated_awarded_movie():
    """
    This function accepts no arguments.
    It retrieves a movie object with the highest rating that has been awarded and its status is "Awarded"
    (is_awarded=True).
    """

    movie = Movie.objects.order_by('-rating', 'title').filter(is_awarded=True).first()

    if not movie:
        return ''

    return (f"Top rated awarded movie: "
            f"{movie.title}, "
            f"rating: {round(movie.rating, 1)}. "
            f"Starring actor: {movie.starring_actor.full_name if movie.starring_actor else 'N/A'}. "
            f"Cast: {', '.join(actor.full_name for actor in movie.actors.order_by('full_name'))}")


def increase_rating():
    """
    It increases the rating for all movies that are considered classic – their status is "Classic" (is_classic=True)
    and their rating is not already set to the maximum level.
    Increase the rating by 0.1 (zero point one).
    """

    classics = Movie.objects.all().filter(is_classic=True, rating__lt=10)

    for movie in classics:
        movie.rating += Decimal(0.1)

    Movie.objects.bulk_update(classics, ['rating',])

    return f"Rating increased for {classics.count()} movies." if classics else 'No ratings increased.'


# print(Director.objects.get_directors_by_movies_count())
# print(get_directors(search_name=None, search_nationality='bu'))
# print(get_top_director())
# print(get_top_actor())
# print(get_actors_by_movies_count())
print(get_top_rated_awarded_movie())
# print(increase_rating())
