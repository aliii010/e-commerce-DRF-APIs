from django.db import models
from django.contrib.auth import get_user_model
from users.models import Address
from products.models import ProductItem


class Order(models.Model):
  user_model = get_user_model()
  customer = models.ForeignKey(user_model, on_delete=models.PROTECT)
  date = models.DateField(db_index=True, null=True, blank=True)
  shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
  status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)

  def get_total_price(self):
    return sum(item.get_price() for item in self.order_items.all()) # order_items is the related name

  def __str__(self):
    return f"{self.customer.first_name}'s order ({self.id})"


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name='menuitems')
  qty = models.SmallIntegerField()

  def get_price(self):
    return self.product_item.price * self.qty


class OrderStatus(models.Model):
  status = models.CharField(max_length=55)

  def __str__(self):
    return self.status