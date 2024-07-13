from django.contrib import admin
from .models import Address, UserAccount

admin.site.register(UserAccount)
admin.site.register(Address)
