# crm/models.py
from django.db import models
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Save the order first
        super().save(*args, **kwargs)
        
        # Calculate total amount if products are assigned
        if self.products.exists():
            total = sum(product.price for product in self.products.all())
            self.total_amount = total
            super().save(update_fields=['total_amount'])

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

    class Meta:
        ordering = ['-order_date']