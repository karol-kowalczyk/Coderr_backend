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

class OfferDetails(models.Model):
   
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=150)
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPES)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Offerdetails'

class Orders(models.Model):
   
    customer_user = models.ForeignKey(User, related_name='customer_order', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'customer'})
    business_user = models.ForeignKey(User, related_name='business_order', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'business'})
    offer = models.ForeignKey('Offers', on_delete=models.CASCADE, related_name='orders')
    offer_details = models.ForeignKey('OfferDetails', on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=150)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25)

    def __str__(self):
        return f'Order by {self.customer_user.username} for {self.title}'
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Orders'

class Reviews(models.Model):

    customer_user = models.ForeignKey(User, related_name='customer_reviews', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'customer'})
    business_user = models.ForeignKey(User, related_name='business_reviews', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'business'})
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.business_user} by {self.customer_user}'
    
    class Meta:
        ordering = ['rating']
        verbose_name_plural = 'Reviews'