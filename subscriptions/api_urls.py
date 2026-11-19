from django.urls import path
from . import api_views

urlpatterns = [
    path(
        '',
        api_views.subscription_list_create,
        name='subscription-list-create'
    ),
    path(
        '<int:pk>/',
        api_views.subscription_detail,
        name='subscription-detail'
    ),
]
