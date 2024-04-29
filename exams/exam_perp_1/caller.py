import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order
from django.db.models import Q


# Create and run your queries within functions
#
# user1 = Profile.objects.get_or_create(
#     full_name='Stan Do',
#     email='stan@do.com',
#     phone_number='0123456789',
#     address='123 Main Street',
# )
#
# user2 = Profile.objects.get_or_create(
#     full_name='Test User',
#     email='user@test.com',
#     phone_number='1125544778',
#     address='123 Hollywood boulevard',
# )
#
# user3 = Profile.objects.get_or_create(
#     full_name='Muci Smirnenski',
#     email='muci@smirnenski.com',
#     phone_number='+5988777878',
#     address='3 Tepl Str',
# )
#
# product1 = Product.objects.get_or_create(
#     name='Test Product',
#     description='Some description',
#     price=11.23,
#     in_stock=10,
# )
# product2 = Product.objects.get_or_create(
#     name='Soap',
#     description='For most delicate piece of skin!',
#     price=99.99,
#     in_stock=1,
# )
# product3 = Product.objects.get_or_create(
#     name='Shampoo',
#     description='Hair body face',
#     price=5.75,
#     in_stock=20,
# )
#

def get_profiles(search_string=None):
    """
    It retrieves profile objects by partially and case-insensitively matching the given searching criteria for
    full name, email, or phone number. Check if any of these three field values (full name, email, or phone number)
    contain the search string.
    Order the profile objects by full name, ascending.
     """
    if search_string:
        query = (Q(full_name__icontains=search_string) |
                 Q(email__icontains=search_string) |
                 Q(phone_number__icontains=search_string))

        all_profile_objs = Profile.objects.all().filter(query).prefetch_related('orders').order_by('full_name')

    else:
        all_profile_objs = Profile.objects.all().order_by('full_name')

    result = []
    for obj in all_profile_objs:
        result.append(f'Profile: {obj.full_name}, email: {obj.email},'
                      f' phone number: {obj.phone_number}, orders: {obj.orders.count()}')

    return '\n'.join(result) if result else ''


def get_loyal_profiles():
    """
    This function accepts no arguments.
    It retrieves profile objects with more than two orders, ordered by number of orders, descending.
    You should count all orders regardless of their status ("Completed" or "Not Completed").
    """
    all_profiles = Profile.objects.get_regular_customers()
    result = []
    for obj in all_profiles:
        result.append(f"Profile: {obj.full_name}, orders: {obj.orders.count()}")

    return '\n'.join(result) if result else ''


def get_last_sold_products():
    """
    This function accepts no arguments.
    It retrieves the products from the latest order object, ordered by product name, ascending.
    The status of the order does not matter ("Completed" or "Not Completed").
    """
    last_order = Order.objects.order_by('-creation_date').first()

    if not last_order:
        return ""

    products = last_order.products.all().order_by('name')
    result = [product.name for product in products]

    return f"Last sold products: {', '.join(result)}"


# print(get_profiles())
# print(get_loyal_profiles())
# print(get_last_sold_products())
