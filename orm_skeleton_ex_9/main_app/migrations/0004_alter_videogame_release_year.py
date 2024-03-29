# Generated by Django 4.2.4 on 2024-01-29 21:08

from django.db import migrations, models
import main_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_videogame_release_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogame',
            name='release_year',
            field=models.PositiveIntegerField(validators=[main_app.validators.RangeValidator(max_value=2023, message='The release year must be between 1990 and 2023', min_value=1990)]),
        ),
    ]
