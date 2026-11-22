from django.urls import path
from . import api_views

urlpatterns = [
    path(
        '',
        api_views.subscription_list_create,
        name='subscription-list-create'
    ),
    path(
        'history/', 
         api_views.subscription_history, 
         name='subscription-history'
    ),
    path(
        'calendar/',
         api_views.renewal_calendar,
         name='renewal-calendar'
    ),
    path(
        '<int:pk>/',
        api_views.subscription_detail,
        name='subscription-detail'
    ),
]
