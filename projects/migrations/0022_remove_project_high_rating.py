# Generated by Django 3.1.1 on 2022-09-27 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_project_high_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='high_rating',
        ),
    ]
