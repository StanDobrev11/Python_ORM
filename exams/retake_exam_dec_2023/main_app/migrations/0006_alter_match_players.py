# Generated by Django 4.2.4 on 2024-08-01 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_match_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(related_name='matches', to='main_app.tennisplayer'),
        ),
    ]
