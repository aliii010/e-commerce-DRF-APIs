# Generated by Django 5.0.6 on 2024-05-20 19:25

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_useraccount_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
