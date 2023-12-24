import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop


# Create and check models
def bulk_create_arts(*args):
    ArtworkGallery.objects.bulk_create(args)


def show_highest_rated_art():
    art = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{art.art_name} is the highest-rated art with a {art.rating} rating!"


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def bulk_create_laptops(args):
    for arg in args:
        arg.save()


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo', 'Dell']).update(memory=16)


def update_operation_systems():
    all_laptops = Laptop.objects.all()

    for laptop in all_laptops:
        if laptop.brand == 'Asus':
            laptop.operation_system = 'Windows'
        elif laptop.brand == 'Apple':
            laptop.operation_system = 'MacOS'
        elif laptop.brand == 'Acer' or laptop.brand == 'Dell':
            laptop.operation_system = 'Linux'
        else:
            laptop.operation_system = 'Chrome OS'

    Laptop.objects.bulk_update(all_laptops, ['operation_system'])


def show_the_most_expensive_laptop():
    laptop = Laptop.objects.order_by('-price', '-pk').first()
    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"

# Run and print your queries
# print(show_the_most_expensive_laptop())
# laptop1 = Laptop(
#     brand='Asus', processor='Intel Core i5', memory=8, storage=256, operation_system='Windows', price=899.99)
# laptop2 = Laptop(
#     brand='Apple', processor='Apple M1', memory=16, storage=512, operation_system='MacOS', price=1399.99)
# laptop3 = Laptop(
#     brand='Lenovo', processor='AMD Ryzen 7', memory=12, storage=512, operation_system='Linux', price=999.99)
# Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
# Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)  # Execute the following functions
# update_to_512_GB_storage()
# update_operation_systems()
# Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)

# artwork1 = ArtworkGallery(artist_name="Vincent van Gogh", art_name="Starry Night", rating=4, price=7500000.0)
# artwork2 = ArtworkGallery(artist_name="Leonardo da Vinci", art_name="Mona Lisa", rating=5, price=1900000.0)
# artwork3 = ArtworkGallery(artist_name="Michelangelo", art_name="Chapel", rating=1, price=800000.0)
# artwork4 = ArtworkGallery(artist_name="Einstein", art_name="Nuke", rating=2, price=11500000.0)
# artwork5 = ArtworkGallery(artist_name="Ivan Vazov", art_name="Pod Igoto", rating=5, price=150000.0)
# bulk_create_arts(artwork1, artwork2, artwork3, artwork4, artwork5)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())
