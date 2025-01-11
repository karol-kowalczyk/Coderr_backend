
from rest_framework import serializers
from django.contrib.auth.models import User
from coderr_app.models import models


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'password_repeat', 'role']
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Der Benutzername ist bereits vergeben.")

        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_repeat')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        user_profile = UserProfile.objects.create(
            user=user,
            role=validated_data['role']
        )

        return user_profile