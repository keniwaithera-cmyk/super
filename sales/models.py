from django.db import models

# Create your models here.
# sales/models.py
from django.db import models
from inventory.models import Product
from customers.models import Customer


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_sold = models.PositiveIntegerField()
    sold_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

def total_price(self):
        return self.product.price * self.quantity_sold


