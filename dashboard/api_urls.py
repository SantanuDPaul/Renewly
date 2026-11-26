from django.urls import path
from . import api_views

urlpatterns = [
    path('analytics/', api_views.dashboard_analytics, name='dashboard-analytics'),
    path('budget/', api_views.monthly_budget, name='monthly-budget'),
]