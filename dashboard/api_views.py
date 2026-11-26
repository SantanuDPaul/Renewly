from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.response import Response

from subscriptions.models import Subscription

from rest_framework import status
from .models import MonthlyBudget
from .serializers import MonthlyBudgetSerializer


@api_view(['GET'])
def dashboard_analytics(request):
    subscriptions = Subscription.objects.filter(
        user=request.user,
        status='ACTIVE'
    )

    currency_totals = {}
    for subscription in subscriptions:
        currency = subscription.currency

        if currency not in currency_totals:
            currency_totals[currency] = {
                'monthly': Decimal('0.00'),
                'yearly': Decimal('0.00'),
            }

        if subscription.billing_cycle == 'MONTHLY':
            currency_totals[currency]['monthly'] += subscription.price
        elif subscription.billing_cycle == 'YEARLY':
            currency_totals[currency]['yearly'] += subscription.price

    analytics = {}

    for currency, totals in currency_totals.items():
        monthly = totals['monthly']
        yearly = totals['yearly']

        analytics[currency] = {
            'monthly_total': str(monthly),
            'yearly_total': str(yearly),
            'estimated_monthly_spending': str(
                round(monthly + yearly / Decimal('12'), 2)
            ),
            'estimated_yearly_spending': str(
                round(monthly * Decimal('12') + yearly, 2)
            ),
        }
        budget = MonthlyBudget.objects.filter(
            user=request.user
        ).first()

        budget_summary = None

        if budget:
            currency_data = analytics.get(budget.currency, {})

            monthly_spending = Decimal(
                currency_data.get('estimated_monthly_spending', '0.00')
            )

            remaining = budget.amount - monthly_spending

            percentage_used = (
                (monthly_spending / budget.amount) * 100
                if budget.amount > 0
                else Decimal('0')
            )

            budget_summary = {
                'currency': budget.currency,
                'budget_amount': str(budget.amount),
                'monthly_spending': str(monthly_spending),
                'remaining': str(round(remaining, 2)),
                'percentage_used': round(percentage_used, 2),
                'is_over_budget': monthly_spending > budget.amount,
            }

    return Response({
        'active_subscriptions': subscriptions.count(),
        'currency_analytics': analytics,
        'budget_summary': budget_summary,
    })

@api_view(['GET', 'PUT'])
def monthly_budget(request):
    budget = MonthlyBudget.objects.filter(
        user=request.user
    ).first()

    if request.method == 'GET':
        if budget is None:
            return Response({
                'message': 'No monthly budget set.'
            })

        serializer = MonthlyBudgetSerializer(budget)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MonthlyBudgetSerializer(
            budget,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=(
                    status.HTTP_200_OK
                    if budget
                    else status.HTTP_201_CREATED
                )
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )