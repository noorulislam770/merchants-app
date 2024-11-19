from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    outstanding_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Transaction (models.Model):
    TRANSACTION_TYPES = [
        ('sale', 'Sale'),
        ('expense', 'Expense'),
        ('credit', 'Credit'),

    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    salesperson = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE,
        related_name='transactions_as_salesperson')
    edited_on = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE,
        related_name='transactions_as_edited_by'
    )
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount}"
