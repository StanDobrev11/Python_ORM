import os
from decimal import Decimal

import django
from django.db.models import Sum, F, Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


# Create and check models
# def add_records_to_database():
#     # Categories
#     food_category = Category.objects.create(name='Food')
#     drinks_category = (Category.objects.create(name='Drinks'))
#
#     # Food
#     product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99, category=food_category, is_available=False)
#     product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99, category=food_category, is_available=False)
#     product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99, category=food_category, is_available=True)
#     product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49, category=food_category, is_available=True)
#     product5 = Product.objects.create(name='Pasta and Sauce Bundle', description='Package containing pasta and a jar of pasta sauce', price=6.99, category=food_category, is_available=False)
#     product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99, category=food_category, is_available=True)
#     product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs', price=3.49, category=food_category, is_available=True)
#     product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99, category=food_category, is_available=False)
#     product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49, category=food_category, is_available=True)
#
#     # Drinks
#     product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99, category=drinks_category, is_available=True)
#     product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49, category=drinks_category, is_available=False)
#     product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water', price=4.99, category=drinks_category, is_available=True)
#     product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49, category=drinks_category, is_available=True)
#     product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99, category=drinks_category, is_available=False)
#     product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49, category=drinks_category, is_available=True)
#
#     # Customers
#     customer1 = Customer.objects.create(username='john_doe')
#     customer2 = Customer.objects.create(username='alex_alex')
#     customer3 = Customer.objects.create(username='peter132')
#     customer4 = Customer.objects.create(username='k.k.')
#     customer5 = Customer.objects.create(username='peter_smith')
#
#     # Orders
#     order1 = Order.objects.create(customer=customer1)
#     order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
#     order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
#     order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
#     order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)
#
#     order2 = Order.objects.create(customer=customer3)
#     order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
#     order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)
#
#     order3 = Order.objects.create(customer=customer1)
#     order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
#     order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
#     return "All data entered!"
#

def product_quantity_ordered():
    """
    returns a summary of the total quantity ordered for each product available only for products that have at least
    one unit ordered, arranged in descending order based on the total quantity ordered
    """

    # min_one_order = OrderProduct.objects.values('product__name').annotate(
    #     ttl_quantity=Sum('quantity')
    # ).filter(ttl_quantity__gte=1).order_by('-ttl_quantity')

    min_one_order = Product.objects.annotate(
        ttl_quantity=Sum('orderproduct__quantity')
    ).exclude(ttl_quantity=0).order_by('-ttl_quantity')

    ll = []
    for product in min_one_order:
        # ll.append(f"Quantity ordered of {product['product__name']}: {product['ttl_quantity']}")
        ll.append(f"Quantity ordered of {product.name}: {product.ttl_quantity}")

    return '\n'.join(ll)


def ordered_products_per_customer_slow():
    """
    returns a summary of each ordered product by each customer, arranged in ascending order by the order ID.
    """

    # example using 'for-loops' -> too many queries to DB, not optimized

    orders = Order.objects.all().order_by('id')

    orders_list = []
    for order in orders:
        orders_list.append(f"Order ID: {order.pk}, Customer: {order.customer.username}")
        all_products_in_order = order.products.all()
        for product in all_products_in_order:
            orders_list.append(f"- Product: {product.name}, Category: {product.category.name}")

    return '\n'.join(orders_list)


def ordered_products_per_customer():
    # example using pre-fetch - when have many-to-many relations
    orders = Order.objects.prefetch_related(
        'customer',  # get related customer
        'products',  # get all products in order
        'products__category',  # get all categories for each product
    ).order_by('id')

    orders_list = []
    for order in orders:
        orders_list.append(f"Order ID: {order.pk}, Customer: {order.customer.username}")
        all_products_in_order = order.products.all()
        for product in all_products_in_order:
            orders_list.append(f"- Product: {product.name}, Category: {product.category.name}")

    return '\n'.join(orders_list)


def filter_products():
    """
    returns information for all available products with prices greater than 3.00
    Arranges the information in descending order by the price.
    If there are two or more products with the same price, orders them by name in ascending order (alphabetically).
    """
    products = Product.objects.filter(price__gt=3, is_available=True).order_by('-price', 'name')

    result = []
    for product in products:
        result.append(f"{product.name}: {product.price}lv.")

    return '\n'.join(result)


def give_discount():
    """
    reduces the product's price by 30% of all available products with prices greater than 3.00
    Arranges the information in descending order by the price.
    If there are two or more products with the same price, orders them by name in ascending order (alphabetically).
    """

    query = Q(price__gt=3) & Q(is_available=True)
    price_reduction = F('price') * 0.7
    products = Product.objects.filter(query).order_by('-price', 'name')
    products.update(price=price_reduction)

    result = []
    for product in products:
        result.append(f"{product.name}: {product.price :.2f}lv.")

    return '\n'.join(result)


# Run and print your queries
#
# print('All Products:')
# print(Product.objects.all())
# print()
# print('All Available Products:')
# print(Product.objects.available_products())
# print()
# print('All Available Food Products:')
# print(Product.objects.available_products_in_category("Food"))

# print(product_quantity_ordered())
# print(ordered_products_per_customer_slow())
# print(ordered_products_per_customer())
# print(filter_products())
print(give_discount())
