from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """
    Custom user model.
    Keeping it simple for Version 1.
    We'll extend it in future versions.
    """

    def __str__(self):
        return self.username