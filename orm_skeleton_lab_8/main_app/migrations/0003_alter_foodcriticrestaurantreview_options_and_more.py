# Generated by Django 4.2.4 on 2024-01-15 19:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_foodcriticrestaurantreview_regularrestaurantreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodcriticrestaurantreview',
            options={'ordering': ['-rating'], 'verbose_name': 'Food Critic Review', 'verbose_name_plural': 'Food Critic Reviews'},
        ),
        migrations.AlterUniqueTogether(
            name='foodcriticrestaurantreview',
            unique_together={('reviewer_name', 'restaurant')},
        ),
        migrations.CreateModel(
            name='MenuReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_name', models.CharField(max_length=100)),
                ('review_content', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_app_menu_review_menu_id', to='main_app.menu')),
            ],
            options={
                'verbose_name': 'Menu Review',
                'verbose_name_plural': 'Menu Reviews',
                'ordering': ['-rating'],
                'unique_together': {('reviewer_name', 'menu')},
            },
        ),
    ]
