# Generated by Django 4.1.3 on 2022-12-05 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0013_alter_postmodel_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='img',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
