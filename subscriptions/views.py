from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from subscriptions.forms import SubscriptionForm
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date, timedelta
from .models import Category, SubscriptionHistory, HistoryAction

# Create your views here.

class AddSubscriptionView(LoginRequiredMixin, View):
    def get(self, request):

        form= SubscriptionForm()
        context = {
            "title": "Add Subscription",
            "form": form,
        }
        
        return render(request, "subscriptions/add_subscription.html", context)
    
    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user  
            subscription.save()
            SubscriptionHistory.objects.create(
                subscription=subscription,
                action=HistoryAction.CREATED,
            )

            messages.success(request, "Subscription added successfully.")
            return redirect("subscription_list")  
        
        context = {
                "title": "Add Subscription",
                "form": form,
            }
        return render(request, "subscriptions/add_subscription.html", context)

class EditSubscriptionView(LoginRequiredMixin, View):
    def get(self, request, id):
        subscription = get_object_or_404(request.user.subscriptions, id=id)
        form = SubscriptionForm(instance=subscription)
        context = {
            "title": "Edit Subscription",
            "form": form,
        }
        return render(request, "subscriptions/edit_subscription.html", context)

    def post(self, request, id):
        subscription = get_object_or_404(request.user.subscriptions, id=id)
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription updated successfully.")
            return redirect("subscription_list")  
        context = {
            "title": "Edit Subscription",
            "form": form,
        }
        return render(request, "subscriptions/edit_subscription.html", context)

class CancelSubscriptionView(LoginRequiredMixin, View):
    def get(self, request, id):
        subscription = get_object_or_404(request.user.subscriptions, id=id)
        context = {
            "title": "Cancel Subscription",
            "subscription": subscription,
        }
        return render(request, "subscriptions/cancel_subscription.html", context)

    def post(self, request, id):
        subscription = get_object_or_404(request.user.subscriptions, id=id)
        subscription.status = "CANCELLED"
        subscription.save()
        SubscriptionHistory.objects.create(
            subscription=subscription,
            action=HistoryAction.CANCELLED,
        )
        messages.success(request,"Subscription archived successfully.")
        return redirect("subscription_list")
    
class SubscriptionListView(LoginRequiredMixin, View):
    def get(self, request):
        all_subscriptions = request.user.subscriptions.filter(
            status="ACTIVE"
        ) # Get subscriptions for the logged-in user
        subscriptions = all_subscriptions
        search_query = request.GET.get("search","")
        category_filter = request.GET.get("category", "")
        status_filter = request.GET.get("status", "")
        if search_query:
            subscriptions = subscriptions.filter(
                service_name__icontains=search_query
            )
        if category_filter:
            subscriptions = subscriptions.filter(
                category_id=category_filter
            )
        if status_filter:
            subscriptions = subscriptions.filter(
                status=status_filter
            )
        

        today = date.today()
        soon = today + timedelta(days=7)

        sort_by = request.GET.get("sort", "-renewal_date")
        allowed_sorts = [
            "-renewal_date",
            "renewal_date",
            "service_name",
            "-service_name",
            "price",
            "-price",
            "start_date",
            "-start_date",
        ]
        if sort_by not in allowed_sorts:
            sort_by = "-renewal_date"

        subscriptions = subscriptions.order_by(sort_by)

        paginator = Paginator(subscriptions, 5)

        page_number = request.GET.get("page")

        subscriptions = paginator.get_page(page_number)

        categories = Category.objects.all()
        context = {
            "title": "My Subscriptions",
            "subscriptions": subscriptions,
            "search_query": search_query,
            "category_filter": category_filter,
            "status_filter": status_filter,
            "categories": categories,
            "has_subscriptions": all_subscriptions.exists(),
            "today": today,
            "soon": soon,
            "sort_by": sort_by,
        }
        return render(request, "subscriptions/subscription_list.html", context)

class ArchivedSubscriptionListView(LoginRequiredMixin, View):
    def get(self, request):

        subscriptions = (
            request.user.subscriptions
            .filter(status="CANCELLED")
            .order_by("-renewal_date")
        )

        context = {
            "title": "Archived Subscriptions",
            "subscriptions": subscriptions,
        }

        return render(
            request,
            "subscriptions/archive.html",
            context,
        )

class SubscriptionHistoryView(LoginRequiredMixin, View):
    def get(self, request, id):

        subscription = get_object_or_404(
            request.user.subscriptions,
            id=id,
        )

        history = subscription.history.all()

        context = {
            "title": "Subscription History",
            "subscription": subscription,
            "history": history,
        }

        return render(
            request,
            "subscriptions/history.html",
            context,
        )

class DeleteSubscriptionView(LoginRequiredMixin, View):
    def get(self, request, id):
        subscription = get_object_or_404(
            request.user.subscriptions.filter(status="CANCELLED"),
            id=id,
        )

        context = {
            "title": "Delete Subscription",
            "subscription": subscription,
        }

        return render(
            request,
            "subscriptions/delete_subscription.html",
            context,
        )

    def post(self, request, id):
        subscription = get_object_or_404(
            request.user.subscriptions.filter(status="CANCELLED"),
            id=id,
        )

        subscription.delete()

        messages.success(
            request,
            "Subscription deleted permanently."
        )

        return redirect("archive_subscriptions")

class RestoreSubscriptionView(LoginRequiredMixin, View):
    def post(self, request, id):
        subscription = get_object_or_404(
            request.user.subscriptions.filter(status="CANCELLED"),
            id=id,
        )

        subscription.status = "ACTIVE"
        subscription.save()
        SubscriptionHistory.objects.create(
            subscription=subscription,
            action=HistoryAction.RESTORED,
        )

        messages.success(
            request,
            "Subscription restored successfully."
        )

        return redirect("archive_subscriptions")
class RenewSubscriptionView(LoginRequiredMixin, View):
    def get(self, request, id):
        subscription = get_object_or_404(
            request.user.subscriptions.filter(status="ACTIVE"),
            id=id,
        )

        context = {
            "title": "Renew Subscription",
            "subscription": subscription,
        }

        return render(
            request,
            "subscriptions/renew_subscription.html",
            context,
        )

    def post(self, request, id):
        subscription = get_object_or_404(
            request.user.subscriptions.filter(status="ACTIVE"),
            id=id,
        )

        subscription.renew()

        messages.success(
            request,
            f"{subscription.service_name} renewed successfully. Next renewal: {subscription.renewal_date:%d %b %Y}."
        )

        return redirect("subscription_list")
