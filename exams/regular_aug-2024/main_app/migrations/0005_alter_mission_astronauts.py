# Generated by Django 4.2.4 on 2024-08-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_rename_deta_of_birth_astronaut_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='astronauts',
            field=models.ManyToManyField(related_name='missions', to='main_app.astronaut'),
        ),
    ]
