from rest_framework import serializers
from .models import MonthlyBudget


class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = ['id', 'amount', 'currency']
        read_only_fields = ['id']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Monthly budget must be greater than zero."
            )
        return value

    def validate_currency(self, value):
        allowed_currencies = ['INR', 'USD', 'EUR', 'GBP']

        if value not in allowed_currencies:
            raise serializers.ValidationError(
                "Unsupported currency."
            )
        return value