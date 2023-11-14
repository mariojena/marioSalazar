# Generated by Django 4.1.5 on 2023-01-09 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_comment_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='buyers',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='buyers', to=settings.AUTH_USER_MODEL),
        ),
    ]