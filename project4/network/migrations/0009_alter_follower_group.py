# Generated by Django 4.1.5 on 2023-02-03 22:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_rename_followers_follower_alter_comment_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='group',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
