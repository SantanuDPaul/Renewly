from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
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
