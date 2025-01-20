from rest_framework import serializers
from coderr_app.models import UserProfile, OfferDetails, Offers, Orders, Reviews
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at', 'username',
            'first_name', 'last_name', 'pk'
        ]
        read_only_fields = ['created_at']


    def to_representation(self, instance):

        representation = super().to_representation(instance)

        representation['pk'] = instance.user.id
        
        if instance.file:
            file_url = str(instance.file.url)
            if '/media/' in file_url:
                representation['file'] = file_url[file_url.index('media/'):]
            else:
                representation['file'] = None
        
        return representation

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', None)
        instance = super().update(instance, validated_data)

        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        return instance
    
class UserSerializer(serializers.ModelSerializer):

    file = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'file']

    def get_file(self, obj):

        user_profile = UserProfile.objects.filter(user=obj).first()
        return user_profile.file.url if user_profile and user_profile.file else None

class UserProfileDetailSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = [
            'user', 'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at', 'pk'
        ]
        read_only_fields = ['created_at']

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation['pk'] = instance.user.id
        
        if instance.file:
            file_url = str(instance.file.url)
            if '/media/' in file_url:
                representation['file'] = file_url[file_url.index('media/'):]
            else:
                representation['file'] = None
        
        return representation

class CustomerProfileDetailSerializer(UserProfileDetailSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'file', 'created_at', 'type']

class OfferDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetails
        fields = ['id', 'url', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation['url'] = f'/offerdetails/{instance.id}/'

        representation['price'] = float(instance.price)
        
        return representation