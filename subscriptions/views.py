from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from subscriptions.forms import SubscriptionForm
from django.contrib import messages



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
            subscription.user = request.user  # Associate the subscription with the logged-in user
            subscription.save()
            messages.success(request, "Subscription added successfully.")
            return redirect("subscription_list")  # Redirect to the subscription list after successful creation
        
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
            return redirect("subscription_list")  # Redirect to the subscription list after successful update

        context = {
            "title": "Edit Subscription",
            "form": form,
        }
        return render(request, "subscriptions/edit_subscription.html", context)

class DeleteSubscriptionView(LoginRequiredMixin, View):
    def get(self, request, id):
        subscription = get_object_or_404(request.user.subscriptions, id=id)
        context = {
            "title": "Delete Subscription",
            "subscription": subscription,
        }
        return render(request, "subscriptions/delete_subscription.html", context)

    def post(self, request, id):
        subscription = get_object_or_404(request.user.subscriptions, id=id)
        subscription.delete()
        messages.success(request, "Subscription deleted successfully.")
        return redirect("subscription_list")  # Redirect to the subscription list after successful deletion

class SubscriptionListView(LoginRequiredMixin, View):
    def get(self, request):
        all_subscriptions = request.user.subscriptions.all().order_by("-renewal_date") # Get subscriptions for the logged-in user
        subscriptions = all_subscriptions
        search_query = request.GET.get("search","")
        if search_query:
            subscriptions = subscriptions.filter(
                service_name__icontains=search_query
            )
        context = {
            "title": "My Subscriptions",
            "subscriptions": subscriptions,
            "search_query": search_query,
            "has_subscriptions": all_subscriptions.exists(),
        }
        return render(request, "subscriptions/subscription_list.html", context)