from . import views
from django.urls import path

urlpatterns = [
    path('add/', views.AddSubscriptionView.as_view(), name='add_subscription'),
]