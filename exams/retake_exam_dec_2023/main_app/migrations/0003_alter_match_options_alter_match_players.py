# Generated by Django 4.2.4 on 2024-08-01 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_match_options_alter_match_players_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(related_name='match_players', to='main_app.tennisplayer'),
        ),
    ]
