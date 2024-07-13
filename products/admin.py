from django.contrib import admin
from .models import Product, ProductItem, Variation, VariationOption
from django.contrib import admin



class VariationAdmin(admin.ModelAdmin):
  list_display = ('name', 'id', 'category')

class VariationOptionAdmin(admin.ModelAdmin):
  list_display = ('value', 'id', 'variation')

admin.site.register(Variation, VariationAdmin)
admin.site.register(VariationOption, VariationOptionAdmin)
admin.site.register(ProductItem)
admin.site.register(Product)
