# Generated by Django 5.0.6 on 2024-05-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_image_productitem_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='out_of_stock',
            field=models.BooleanField(default=False),
        ),
    ]
