from django.db import models
from categories.models import ProductCategory

class Product(models.Model):
  category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=255)
  description = models.TextField(max_length=1000)
  image = models.ImageField(upload_to='product-images', null=True)
  base_price = models.FloatField(null=True)
  featured = models.BooleanField(default=False)

  def __str__(self):
    return self.name


class ProductItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  SKU = models.CharField(max_length=255)
  qty_in_stock = models.IntegerField()
  price = models.FloatField()
  variation_options = models.ManyToManyField('VariationOption', related_name='product_items', blank=True)
  out_of_stock = models.BooleanField(default=False)
  image = models.ImageField(upload_to='product-item-images', null=True)

  def __str__(self):
    variation_list = [str(variation) for variation in self.variation_options.all()]
    variations = ', '.join(variation_list)
    return f"{self.product}, {variations}"


class Variation(models.Model):
  category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='variations', null=True)
  name = models.CharField(max_length=100)

  def __str__(self):
    return f"{self.name} - {self.category}"


class VariationOption(models.Model):
  variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
  value = models.CharField(max_length=25)

  def __str__(self):
    return f"{self.value} - {self.variation.category}"
