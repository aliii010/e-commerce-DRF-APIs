# Generated by Django 5.0.6 on 2024-06-08 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('users', '0006_remove_productitem_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.address'),
        ),
    ]
