# Generated by Django 4.2.4 on 2024-05-03 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_movie_actors_alter_movie_director_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='last_updated',
        ),
    ]