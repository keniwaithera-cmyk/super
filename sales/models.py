from django.db import models
from django.db.models import Sum
from django.utils import timezone


# ===========================
# Product Model
# ===========================
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def reduce_stock(self, quantity):
        """Reduce stock when a product is sold"""
        if quantity > self.stock:
            raise ValueError(f"Not enough stock for {self.name}")
        self.stock -= quantity
        self.save()


# ===========================
# Customer Model (optional)
# ===========================
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ===========================
# Transaction Model
# ===========================
class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Transaction #{self.id} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

    def calculate_total(self):
        """Calculate total amount from all items"""
        total = sum(item.get_item_total() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

    @staticmethod
    def total_sales(start_date=None, end_date=None):
        """Return total sales between two dates"""
        qs = Transaction.objects.all()
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        total = qs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        return total


# ===========================
# TransactionItem Model
# ===========================
class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        # Set price_at_sale to current product price if not set
        if not self.price_at_sale:
            self.price_at_sale = self.product.price

        # Reduce product stock automatically
        self.product.reduce_stock(self.quantity)

        super().save(*args, **kwargs)

    def get_item_total(self):
        return self.quantity * self.price_at_sale