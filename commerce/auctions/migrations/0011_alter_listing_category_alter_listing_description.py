# Generated by Django 4.1.5 on 2023-01-11 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('none', 'none'), ('Digital_Music', 'Digital Music'), ('Health_and_household_items', 'Health and household items'), ('Patio,_lawn,_and_garden', 'Patio, lawn, and garden'), ('Sports,_outdoor,_and_fitness_supplies', 'Sports, outdoor, and fitness supplies'), ('Books', 'Books'), ('Clothing,_shoes,_and_jewelry', 'Clothing, shoes, and jewelry'), ('Home_and_kitchen_items', 'Home and kitchen items'), ('Pet_supplies', 'Pet supplies'), ('Beauty_and_personal_care', 'Beauty and personal care'), ('Toys_and_games', 'Toys and games'), ('Tools_and_home_improvement_items', 'Tools and home improvement items'), ('Collectibles_and_fine_arts', 'Collectibles and fine arts'), ('Electronics,_computers,_and_accessories', 'Electronics, computers, and accessories'), ('Office_products', 'Office products'), ('Garden_and_outdoor_items', 'Garden and outdoor items'), ('Kitchen_and_dining_items', 'Kitchen and dining items'), ('Grocery_and_gourmet_food', 'Grocery and gourmet food'), ('Major_appliances', 'Major appliances'), ('Cell_phone_accessories', 'Cell phone accessories'), ('Musical_instruments', 'Musical instruments'), ('Industrial_and_scientific_items', 'Industrial and scientific items'), ('Kindle_store_purchases', 'Kindle store purchases'), ('Other', 'Other')], max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
