from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product, Customer, Transaction, TransactionItem

# Register your models
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(TransactionItem)