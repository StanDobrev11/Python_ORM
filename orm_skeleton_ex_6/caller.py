import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Artist, Song


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
