# Generated by Django 4.1.3 on 2022-12-09 16:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0018_alter_postmodel_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]