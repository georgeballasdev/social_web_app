# Generated by Django 4.1.3 on 2023-02-07 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_alter_grouppost_of_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='img',
            field=models.ImageField(default='/images/no_pic.jpeg', upload_to='images/groups-pics'),
        ),
    ]