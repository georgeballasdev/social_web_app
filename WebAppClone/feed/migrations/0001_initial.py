# Generated by Django 4.1.3 on 2023-02-12 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import feed.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('img', models.ImageField(blank=True, null=True, upload_to=feed.models.group_pic_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_by', to=settings.AUTH_USER_MODEL)),
                ('of_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='groups.group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('of_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.post')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
