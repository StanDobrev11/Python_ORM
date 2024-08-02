# Generated by Django 4.2.4 on 2024-08-01 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_match_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wins', to='main_app.tennisplayer'),
        ),
    ]
