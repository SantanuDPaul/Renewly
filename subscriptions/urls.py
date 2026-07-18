from . import views
from django.urls import path

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('add/', views.AddSubscriptionView.as_view(), name='add_subscription'),
    path('edit/<int:id>/', views.EditSubscriptionView.as_view(), name='edit_subscription'),
    path('delete/<int:id>/', views.DeleteSubscriptionView.as_view(), name='delete_subscription'),
]