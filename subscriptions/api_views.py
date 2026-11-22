from django.core import paginator
from django.db.migrations import serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Subscription, SubscriptionHistory
from .serializers import SubscriptionSerializer, SubscriptionHistorySerializer
from django.shortcuts import get_object_or_404

from django.db.models import Q

@api_view(['GET', 'POST'])
def subscription_list_create(request):

    if request.method == 'GET':
        subscriptions = Subscription.objects.filter(
            user=request.user
        )

        params = request.query_params

        if params.get('billing_cycle'):
            subscriptions = subscriptions.filter(
                billing_cycle=params['billing_cycle']
            )

        if params.get('status'):
            subscriptions = subscriptions.filter(
                status=params['status']
            )

        if params.get('category'):
            subscriptions = subscriptions.filter(
                category_id=params['category']
            )

        if params.get('search'):
            subscriptions = subscriptions.filter(
                Q(service_name__icontains=params['search']) |
                Q(notes__icontains=params['search'])
            )

        allowed_ordering = [
            'price', '-price',
            'renewal_date', '-renewal_date',
            'created_at', '-created_at'
        ]

        if params.get('ordering') in allowed_ordering:
            subscriptions = subscriptions.order_by(
                params['ordering']
            )

        paginator = PageNumberPagination()
        paginated_subscriptions = paginator.paginate_queryset(
            subscriptions,
            request
        )

        serializer = SubscriptionSerializer(
            paginated_subscriptions,
            many=True
        )

        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = SubscriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def subscription_detail(request, pk):

    subscription = get_object_or_404(
        Subscription,
        pk=pk,
        user=request.user
    )

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = SubscriptionSerializer(
            subscription,
            data=request.data,
            partial=request.method == 'PATCH'
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def subscription_history(request):
    history = SubscriptionHistory.objects.filter(
        subscription__user=request.user
    ).order_by('-created_at')

    serializer = SubscriptionHistorySerializer(
        history,
        many=True
    )

    return Response(serializer.data)