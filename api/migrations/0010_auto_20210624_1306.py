# Generated by Django 3.0.5 on 2021-06-24 10:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210624_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
