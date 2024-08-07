# Generated by Django 4.2.4 on 2024-08-03 11:06

import django.core.validators
from django.db import migrations, models
import main_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Astronaut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[main_app.validators.phone_number_validator])),
                ('is_active', models.BooleanField(default=True)),
                ('deta_of_birth', models.DateField(blank=True, null=True)),
                ('spacewalks', models.IntegerField(default=0, validators=[django.core.validators.MinLengthValidator(0)])),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
