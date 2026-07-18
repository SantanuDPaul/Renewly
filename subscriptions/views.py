from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from subscriptions.forms import SubscriptionForm



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
            return redirect("dashboard")  # Redirect to the subscription list after successful creation
        
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
        return redirect("subscription_list")  # Redirect to the subscription list after successful deletion

class SubscriptionListView(LoginRequiredMixin, View):
    def get(self, request):
        subscriptions = request.user.subscriptions.all()  # Get subscriptions for the logged-in user
        context = {
            "title": "My Subscriptions",
            "subscriptions": subscriptions,
        }
        return render(request, "subscriptions/subscription_list.html", context)