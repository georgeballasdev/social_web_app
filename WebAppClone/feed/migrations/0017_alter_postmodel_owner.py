# Generated by Django 4.1.3 on 2022-12-06 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('feed', '0016_alter_postmodel_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.socialuser'),
        ),
    ]