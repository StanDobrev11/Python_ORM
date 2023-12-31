import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal
from django.db.models import Q, Case, When, Value, F


# Create and check models
def bulk_create_arts(*args):
    ArtworkGallery.objects.bulk_create(args)


def show_highest_rated_art():
    art = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{art.art_name} is the highest-rated art with a {art.rating} rating!"


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def bulk_create_laptops(*args):
    Laptop.objects.bulk_create(*args)
    # for arg in args:
    #     arg.save()


def update_to_512_GB_storage():
    Laptop.objects.filter(Q(brand='Asus') | Q(brand='Lenovo')).update(storage=512)  # | -> OR, & -> AND
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)  # same as above


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo', 'Dell']).update(memory=16)


def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand='Asus', then=Value('Windows')),
            When(brand='Apple', then=Value('MacOS')),
            When(brand_in=['Acer', 'Dell'], then=Value('Linux')),
            When(brand='Lenovo', then=Value('Chrome OS')),
            default=F('operation_system')
        )
    )

    # all_laptops = Laptop.objects.all()
    #
    # for laptop in all_laptops:
    #     if laptop.brand == 'Asus':
    #         laptop.operation_system = 'Windows'
    #     elif laptop.brand == 'Apple':
    #         laptop.operation_system = 'MacOS'
    #     elif laptop.brand == 'Acer' or laptop.brand == 'Dell':
    #         laptop.operation_system = 'Linux'
    #     else:
    #         laptop.operation_system = 'Chrome OS'
    #
    # Laptop.objects.bulk_update(all_laptops, ['operation_system'])


def show_the_most_expensive_laptop():
    laptop = Laptop.objects.order_by('-price', '-pk').first()
    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"


def delete_inexpencive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(*args):
    ChessPlayer.objects.bulk_create(*args)


def delete_chess_player():
    ChessPlayer.objects.all().delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)



def set_new_chefs():
    Meal.objects.update(
        chef=Case(
            When(meal_type='Breakfast', then=Value('Gordon Ramsay')),
            When(meal_type='Lunch', then=Value('Julia Child')),
            When(meal_type='Dinner', then=Value('Jamie Oliver')),
            When(meal_type='Snack', then=Value('Thomas Keller'))
        )
    )

def set_new_preparation_times():
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type='Breakfast', then=Value('10 minutes')),
            When(meal_type='Lunch', then=Value('12 minutes')),
            When(meal_type='Dinner', then=Value('15 minutes')),
            When(meal_type='Snack', then=Value('5 minutes'))
        )
    )
# Run and print your queries
# set_new_chefs()
# meal1 = Meal.objects.create(
#
# name="Pancakes",
#
# meal_type="Breakfast",
#
# preparation_time="20 minutes",
#
# difficulty=3,
#
# calories=350,
#
# chef="Jane",
#
# )
#
# meal2 = Meal.objects.create(
#
# name="Spaghetti Bolognese",
#
# meal_type="Dinner",
#
# preparation_time="45 minutes",
#
# difficulty=4,
#
# calories=550,
#
# chef="Sarah",
#
# )
#
# Meal.objects.bulk_create(meal1, meal2)
# change_chess_games_lost()
# delete_chess_player()
# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
#
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
# bulk_create_chess_players([player1, player2])
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
