# Generated by Django 4.1.5 on 2023-01-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]