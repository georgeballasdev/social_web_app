# Generated by Django 4.1.3 on 2023-02-07 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_img_alter_group_members_alter_group_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppost',
            name='of_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='groups.group'),
        ),
    ]