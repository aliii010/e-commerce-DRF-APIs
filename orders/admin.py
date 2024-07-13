from django.contrib import admin
from .models import Order, OrderStatus, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)
