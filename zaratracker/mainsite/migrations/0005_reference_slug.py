# Generated by Django 3.1.6 on 2021-02-15 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0004_remove_reference_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='slug',
            field=models.SlugField(default='url'),
        ),
    ]
