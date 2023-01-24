# Generated by Django 3.1.1 on 2022-09-26 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0019_auto_20220927_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='commentsreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
