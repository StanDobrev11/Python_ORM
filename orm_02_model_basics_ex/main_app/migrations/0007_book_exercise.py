# Generated by Django 4.2.4 on 2023-12-18 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=20)),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_available', models.BooleanField(default=True)),
                ('rating', models.FloatField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('difficulty_level', models.CharField(max_length=20)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('equipment', models.CharField(max_length=90)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('calories_burned', models.PositiveIntegerField()),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
    ]
