from django.conf import settings
from django.db import models


class MonthlyBudget(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='monthly_budget'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        default='INR'
    )

    def __str__(self):
        return f"{self.user.username} - {self.currency} {self.amount}"