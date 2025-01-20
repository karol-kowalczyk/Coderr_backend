from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    
    username = models.EmailField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    repeated_password = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=USER_TYPES)
    
    def __str__(self):
        return self.username

class Offers(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=150)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Offers'
