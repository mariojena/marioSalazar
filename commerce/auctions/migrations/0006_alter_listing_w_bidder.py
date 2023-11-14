# Generated by Django 4.1.5 on 2023-01-10 00:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_buyers_listing_w_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='w_bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyers', to=settings.AUTH_USER_MODEL),
        ),
    ]
