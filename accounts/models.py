from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
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

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount}"
