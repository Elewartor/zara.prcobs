# Generated by Django 3.1.6 on 2021-02-15 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_reference_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='slug',
            field=models.SlugField(default='url'),
        ),
    ]