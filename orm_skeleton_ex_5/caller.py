import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery


# Create and check models
def bulk_create_arts(*args):
    ArtworkGallery.objects.bulk_create(args)


def show_highest_rated_art():
    art = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{art.art_name} is the highest-rated art with a {art.rating} rating!"


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# Run and print your queries
# artwork1 = ArtworkGallery(artist_name="Vincent van Gogh", art_name="Starry Night", rating=4, price=7500000.0)
# artwork2 = ArtworkGallery(artist_name="Leonardo da Vinci", art_name="Mona Lisa", rating=5, price=1900000.0)
# artwork3 = ArtworkGallery(artist_name="Michelangelo", art_name="Chapel", rating=1, price=800000.0)
# artwork4 = ArtworkGallery(artist_name="Einstein", art_name="Nuke", rating=2, price=11500000.0)
# artwork5 = ArtworkGallery(artist_name="Ivan Vazov", art_name="Pod Igoto", rating=5, price=150000.0)
# bulk_create_arts(artwork1, artwork2, artwork3, artwork4, artwork5)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())
