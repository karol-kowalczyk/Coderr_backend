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
    """
    Details eines spezifischen Angebots, z. B. Preis und Typ.

    Attributes:
        offer (Offers): Referenz auf das zugehörige Angebot.
        title (str): Titel des Angebotsdetails, max. 150 Zeichen.
        revisions (int): Anzahl der zulässigen Überarbeitungen, Standard: -1 (unbegrenzt).
        delivery_time_in_days (int): Lieferzeit in Tagen.
        price (DecimalField): Preis für dieses Detailpaket.
        features (JSONField): JSON-Daten für spezifische Merkmale oder Eigenschaften.
        offer_type (str): Typ des Angebotsdetails, entweder 'basic', 'standard' oder 'premium'.
    """
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
