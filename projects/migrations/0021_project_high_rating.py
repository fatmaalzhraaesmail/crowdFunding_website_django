# Generated by Django 3.1.1 on 2022-09-27 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20220927_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='high_rating',
            field=models.FloatField(default=0),
        ),
    ]
