from django.urls import path
from . import api_views

urlpatterns = [
    path(
        'register/',
        api_views.register_user,
        name='api-register'
    ),
    path(
        'profile/',
        api_views.user_profile,
        name='api-profile'
    ),
]