# Generated by Django 4.2.4 on 2024-01-07 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_studentenrollment_alter_student_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentenrollment',
            name='grade',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')], default='F', max_length=1),
        ),
        migrations.CreateModel(
            name='LecturerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('office_location', models.CharField(blank=True, max_length=100, null=True)),
                ('lecturer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.lecturer')),
            ],
        ),
    ]
