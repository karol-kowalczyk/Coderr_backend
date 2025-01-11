from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    ]

    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    email = models.EmailField(models.CharField(max_length=128))
    role = models.CharField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username
