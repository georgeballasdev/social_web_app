# Generated by Django 4.1.3 on 2023-01-25 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='last_edited_at',
        ),
    ]
