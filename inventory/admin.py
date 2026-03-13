from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, Supplier, InventoryTransaction

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(InventoryTransaction)
