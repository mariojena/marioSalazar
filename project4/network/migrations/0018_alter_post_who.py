# Generated by Django 4.1.5 on 2023-02-06 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_alter_profile_cover_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
