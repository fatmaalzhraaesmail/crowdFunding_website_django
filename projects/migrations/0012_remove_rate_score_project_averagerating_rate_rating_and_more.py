# Generated by Django 4.1.1 on 2022-09-21 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0011_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='score',
        ),
        migrations.AddField(
            model_name='project',
            name='averagerating',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rate',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
