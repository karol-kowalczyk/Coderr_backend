from django.contrib import admin
from .models import UserProfile, Offers, OfferDetails, Orders, Reviews

class UserAdmin(admin.ModelAdmin):
    list_filter = ['user__username', 'location']
    list_display = ['user__username', 'email', 'location']

class OfferAdmin(admin.ModelAdmin):
    list_filter = ['user__username', 'created_at']
    list_display = ['title', 'description', 'user__username', 'created_at']

class OfferDetailsAdmin(admin.ModelAdmin):
    list_filter = ['offer', 'title']
    list_display = ['title', 'offer', 'offer__user__username', 'price', 'offer_type']

class OrdersAdmin(admin.ModelAdmin):
    list_filter = ['offer', 'title', 'customer_user', 'business_user', 'status']
    list_display = ['title', 'offer', 'business_user', 'customer_user', 'status', 'offer_type']

class ReviewsAdmin(admin.ModelAdmin):
    list_filter = ['description', 'customer_user', 'business_user']
    list_display = ['description', 'business_user', 'customer_user', 'rating']


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Offers, OfferAdmin)
admin.site.register(OfferDetails, OfferDetailsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Reviews, ReviewsAdmin)