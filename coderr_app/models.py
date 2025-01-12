from django.db import models

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
