from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from subscriptions.models import BillingCycle
from datetime import date, timedelta

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):

        subscriptions = request.user.subscriptions.all()
        total_subscriptions = subscriptions.count()

        monthly_spending = 0
        yearly_spending = 0

        for subscription in subscriptions:

            if subscription.billing_cycle == BillingCycle.MONTHLY:
                monthly_spending += subscription.price
                yearly_spending += subscription.price * 12

            elif subscription.billing_cycle == BillingCycle.YEARLY:
                monthly_spending += subscription.price / 12
                yearly_spending += subscription.price


        today = date.today()
        next_week = today + timedelta(days=7)

        upcoming_renewals = (
            subscriptions.filter(
                status="ACTIVE",
                renewal_date__range=[today, next_week]
            )
            .order_by("renewal_date")
        )

        renewing_soon_count = subscriptions.filter(
            status="ACTIVE",
            renewal_date__range=[today, next_week]
        ).count()

        for subscription in upcoming_renewals:
            subscription.days_left = (
                subscription.renewal_date - today
            ).days

        context = {
        "title": "Dashboard",
        "total_subscriptions": total_subscriptions,
        "monthly_spending": monthly_spending,
        "yearly_spending": yearly_spending,
        "renewing_soon": renewing_soon_count,
        "upcoming_renewals": upcoming_renewals,
        }

        return render(
        request,
        "dashboard/home.html",
        context,
        )