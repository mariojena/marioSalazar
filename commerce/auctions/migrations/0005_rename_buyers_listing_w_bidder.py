# Generated by Django 4.1.5 on 2023-01-10 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_buyers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='buyers',
            new_name='w_bidder',
        ),
    ]
