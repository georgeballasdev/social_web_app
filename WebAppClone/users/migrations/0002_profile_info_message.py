# Generated by Django 4.1.4 on 2023-02-14 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='info_message',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]