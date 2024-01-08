import os
from datetime import date, timedelta

import django
from django.db.models import Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, Car


# Create queries within functions
def show_all_authors_with_their_books():
    all_authors = Author.objects.all()  # better way is to use prefetch

    result = []
    for author in all_authors:
        author_books = author.book_set.all()
        if len(author_books) == 0:
            continue
        result.append(f"{author} has written - {', '.join(str(book) for book in author_books)}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    """ gets the artist object by the artist's name and the song object by the song's title,
    and adds the song object to the artist's songs collection."""

    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    """returns all the song objects from the songs collection, ordered by song id (descending) for the given artist."""

    artist = Artist.objects.get(name=artist_name)

    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    """gets the artist object by the artist's name and the song object by the song's title,
    and removes the song object from the artist's songs collection."""

    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    """returns the calculated average rating for a given product by its name."""

    # product = Product.objects.get(name=product_name)
    # return Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']

    product = Product.objects.annotate(avg_rating=Avg('reviews__rating')).get(name=product_name)
    return product.avg_rating


def get_reviews_with_high_ratings(threshold: int):
    """returns all reviews with greater than or equal ratings than the threshold."""

    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    """returns all products that do NOT have any related reviews, ordered by product name (descending)."""

    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    """deletes all the products that do not have any related reviews."""

    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    """calculates the expiration date for all licenses. The expiration date is 365 days after the issue date.
    Return the license number and the expiration date as a string, ordered by license number (descending)"""

    all_licenses = DrivingLicense.objects.all().order_by('-license_number')

    result = []

    for license in all_licenses:
        result.append(
            f"License with id: {license.license_number} expires on {license.get_exp_date()}!")

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date):
    """returns all drivers (in a list) that have expired licenses.
    A license counts as expired when the expiration date is one or more days after the due date."""

    drivers_with_exp_licenses = Driver.objects.filter(drivinglicense__issue_date__gt=due_date - timedelta(days=365))

    return drivers_with_exp_licenses


def register_car_by_owner(owner: object):
    """that register cars with the given owner object"""

    first_reg = Registration.objects.filter(car__isnull=True).order_by('registration_date').first()
    first_car = Car.objects.filter(registration__isnull=True).first()

    first_car.owner = owner
    first_car.save()

    first_reg.car = first_car
    first_reg.registration_date = date.today()
    first_reg.save()

    return f"Successfully registered {first_car} to {owner} with registration number {first_reg}."

