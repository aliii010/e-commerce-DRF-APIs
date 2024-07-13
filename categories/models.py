from django.db import models

class ProductCategory(models.Model):
  parent_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
  category_name = models.CharField(max_length=55)

  def __str__(self):
    return self.category_name