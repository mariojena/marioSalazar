# Generated by Django 4.1.5 on 2023-02-06 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_alter_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_photo',
            field=models.URLField(blank=True),
        ),
    ]
