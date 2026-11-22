from rest_framework import serializers
from .models import Subscription, SubscriptionHistory


class SubscriptionSerializer(serializers.ModelSerializer):
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value
    def validate(self, data):
        start_date = data.get(
            'start_date',
            self.instance.start_date if self.instance else None
        )

        renewal_date = data.get(
            'renewal_date',
            self.instance.renewal_date if self.instance else None
        )

        if start_date and renewal_date:
            if renewal_date <= start_date:
                raise serializers.ValidationError({
                    "renewal_date": "Renewal date must be after the start date."
                })

        return data
    def validate_service_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Service name cannot be empty."
            )

        return value.strip()
    class Meta:
        model = Subscription
        fields = [
            'id',
            'service_name',
            'category',
            'price',
            'billing_cycle',
            'currency',
            'start_date',
            'renewal_date',
            'payment_method',
            'website',
            'notes',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'status',
            'created_at',
            'updated_at',
        ]
class SubscriptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionHistory
        fields = [
            'id',
            'subscription',
            'action',
            'old_renewal_date',
            'new_renewal_date',
            'created_at',
        ]

        read_only_fields = fields
