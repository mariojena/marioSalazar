# Generated by Django 4.1.5 on 2023-02-15 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0021_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
