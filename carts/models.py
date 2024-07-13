from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductItem


class Cart(models.Model):
  user_model = get_user_model()
  customer = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='carts')

  def get_total_price(self):
    return sum(item.get_price() for item in self.cart_items.all()) # cart_items is the related name

  def __str__(self):
    return f"{self.customer.first_name} {self.customer.last_name}'s cart"


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name='cart_items')
  qty = models.IntegerField()

  def get_price(self):
    return self.product_item.price * self.qty