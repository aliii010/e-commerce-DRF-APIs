# Generated by Django 5.0.6 on 2024-06-24 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
