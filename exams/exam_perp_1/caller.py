import os
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count


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
# product4 = Product.objects.get_or_create(
#     name='Cream',
#     description='Nivea',
#     price=7.75,
#     in_stock=10,
# )
# product5 = Product.objects.get_or_create(
#     name='Nivea',
#     description='Hand Cream',
#     price=2.75,
#     in_stock=10,
# )
#
# product6 = Product.objects.get_or_create(
#     name='Fungicid',
#     description='Fungi',
#     price=7.75,
#     in_stock=10,
# )
def get_profiles(search_string=None):
    """
    It retrieves profile objects by partially and case-insensitively matching the given searching criteria for
    full name, email, or phone number. Check if any of these three field values (full name, email, or phone number)
    contain the search string.
    Order the profile objects by full name, ascending.
     """

    if search_string is None:
        return ''

    query = (Q(full_name__icontains=search_string) |
             Q(email__icontains=search_string) |
             Q(phone_number__icontains=search_string))

    profiles = Profile.objects.filter(query).order_by('full_name')

    return '\n'.join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_loyal_profiles():
    """
    This function accepts no arguments.
    It retrieves profile objects with more than two orders, ordered by number of orders, descending.
    You should count all orders regardless of their status ("Completed" or "Not Completed").
    """

    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    return '\n'.join(
        f"Profile: {p.full_name}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_last_sold_products():
    """
    This function accepts no arguments.
    It retrieves the products from the latest order object, ordered by product name, ascending.
    The status of the order does not matter ("Completed" or "Not Completed").
    """
    last_order = Order.objects.prefetch_related('products').last()

    if not last_order or not last_order.products.exists():
        return ""

    result = [product.name for product in last_order.products.order_by('name')]

    return f"Last sold products: {', '.join(result)}"


def get_top_products():
    """
    It retrieves the most frequently sold products from all orders.
    Order them by the number of times the product has been sold (included in an order), descending,
    then ascending by product name. The status of the orders does not matter ("Completed" or "Not Completed").
    Take the top five ordered products.
    """
    orders = Order.objects.prefetch_related('products')

    if not orders:
        return ''

    products = {}

    for order in orders:
        for product in order.products.all():
            if product.name not in products:
                products[product.name] = 1
            else:
                products[product.name] += 1

    if not products:
        return ''

    result = ['Top products:']
    for product, sold in sorted(products.items(), key=lambda x: (-x[1], x[0])):
        result.append(f"{product}, sold {sold} times")

    return '\n'.join(result[:6])


def apply_discounts():
    """
    It retrieves order objects that have more than two products,
    whose status is "Not Completed" (is_completed=False), and applies a discount of 10% to the total price.
    """
    orders = Order.objects.annotate(total_products=Count('products')).filter(is_completed=False, total_products__gt=2)

    for order in orders:
        order.total_price *= Decimal(0.9)

    Order.objects.bulk_update(orders, ['total_price'])

    return f"Discount applied to {orders.count()} orders."


def complete_order():
    """
    It retrieves the first (oldest) order object from your database whose status is "Not Completed"
    and changes it from "Not Completed" (is_completed=False) to "Completed" (is_completed=True).
    Remember that you must decrease the quantity of the ordered products you have in stock (in_stock).
    If a quantity becomes 0 (zero), change the status of the product to "Not Available" (is_available=False).
    """

    order = Order.objects.prefetch_related('products').filter(is_completed=False).first()

    if not order:
        return ''

    order.is_completed = True

    for product in order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False


    Product.objects.bulk_update(order.products.all(), ['in_stock', 'is_available'])
    order.save()

    return "Order has been completed!"


# print(get_profiles())
# print(get_loyal_profiles())
# print(get_last_sold_products())
# print(get_top_products())
# print(apply_discounts())
# print(complete_order())
