# Generated by Django 4.2.4 on 2023-12-20 00:30
import random

from django.db import migrations


def add_barcode(app, schema_editor):
    Product = app.get_model("main_app", "Product")
    all_products = Product.objects.all()
    all_barcodes = random.sample(
        range(100_000_000, 999_999_999),
        len(all_products)
    )
    for i in range(len(all_products)):
        product = all_products[i]
        product.barcode = all_barcodes[i]
        product.save()

    print(all_barcodes)


def reverse_add_barcode(app, schema_editor):
    Product = app.get_model("main_app", "Product")
    Product.objects.all().update(barcode=0)

    print('Reversed')
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0004_product_barcode'),
    ]

    operations = [
        migrations.RunPython(add_barcode, reverse_add_barcode)
    ]
