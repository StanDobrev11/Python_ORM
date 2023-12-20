# Generated by Django 4.2.4 on 2023-12-20 20:02

from django.db import migrations


def get_rarity_by_price(price):
    if price <= 10:
        return 'Rare'
    elif price <= 20:
        return 'Vary Rare'
    elif price <= 30:
        return 'Extremely Rare'
    else:
        return 'Mega Rare'


def populate_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')
    all_items = item_model.objects.all()

    for item in all_items:
        item.rarity = get_rarity_by_price(item.price)

    item_model.objects.bulk_update(all_items, ['rarity'])


def reverse_populate_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')
    all_items = item_model.objects.all()

    rarity_default = item_model._meta.get_field('rarity').default

    for item in all_items:
        item.rarity = rarity_default

    item_model.objects.bulk_update(all_items, ['rarity'])


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(populate_rarity, reverse_populate_rarity)
    ]
