from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
            ordering = ['name']
            verbose_name_plural = "Categories"


    def __str__(self):
        return self.name
    
class BillingCycle(models.TextChoices):
    MONTHLY = 'MONTHLY', 'Monthly'
    YEARLY = 'YEARLY', 'Yearly'

class Currency(models.TextChoices):
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    INR = 'INR', 'INR'

class PaymentMethod(models.TextChoices):
    CREDIT_CARD = 'CREDIT_CARD', 'Credit Card'
    DEBIT_CARD = 'DEBIT_CARD', 'Debit Card'
    UPI = 'UPI', 'UPI'
    PAYPAL = 'PAYPAL', 'PayPal'
    BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'

class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Subscription(models.Model):
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=50, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.INR)
    start_date = models.DateField()
    renewal_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    website = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='subscriptions')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE,)

class Meta:
    ordering = ['renewal_date']
    verbose_name_plural = "Subscriptions"


def __str__(self):
    return self.service_name
