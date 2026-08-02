from . import views
from django.urls import path

urlpatterns = [
    path("", views.SubscriptionListView.as_view(), name="subscription_list",),
    path("add/", views.AddSubscriptionView.as_view(), name="add_subscription",),
    path("edit/<int:id>/", views.EditSubscriptionView.as_view(), name="edit_subscription",),
    path("cancel/<int:id>/", views.CancelSubscriptionView.as_view(), name="cancel_subscription",),
    path("delete/<int:id>/",views.DeleteSubscriptionView.as_view(),name="delete_subscription",),
    path("archive/", views.ArchivedSubscriptionListView.as_view(), name="archive_subscriptions",),
    path("restore/<int:id>/",views.RestoreSubscriptionView.as_view(),name="restore_subscription",),
    path("renew/<int:id>/",views.RenewSubscriptionView.as_view(),name="renew_subscription",),
    path("history/<int:id>/",views.SubscriptionHistoryView.as_view(),name="subscription_history",),
]