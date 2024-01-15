# Generated by Django 4.2.4 on 2024-01-14 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_regularreservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]