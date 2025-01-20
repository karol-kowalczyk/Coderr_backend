from rest_framework import serializers
from django.contrib.auth.models import User
from coderr_app.models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):

    def validate_unique_username(value):
       
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Bitte prüfe deine Eingaben. Email und/oder Benutzername bereits vergeben.')
        return value

    username = serializers.CharField(validators=[validate_unique_username])
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


    def save(self):
       
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email_exists = User.objects.filter(email=self.validated_data['email']).exists()

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': ['Die Passwörter sind nicht identisch.']})
        if email_exists:
            raise serializers.ValidationError({'error': ['Bitte prüfe deine Eingaben. Email und/oder Benutzername bereits vergeben.']})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()

        UserProfile.objects.create(
            user=account,
            email=self.validated_data['email'],
            type=self.validated_data['type']
        )

        return account