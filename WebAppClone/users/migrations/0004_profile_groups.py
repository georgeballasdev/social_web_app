# Generated by Django 4.1.3 on 2023-02-08 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_rename_created_at_group_timestamp'),
        ('users', '0003_profile_latest_posts_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='groups', to='groups.group'),
        ),
    ]
