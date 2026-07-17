from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):

        context = {
        "title": "Dashboard",
        "user": request.user,
        }

        return render(
        request,
        "dashboard/home.html",
        context,
        )