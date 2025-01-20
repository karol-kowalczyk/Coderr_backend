from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status

class RegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response(data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
  
    permission_classes = [AllowAny]

    def post(self, request, *arg, **kwarg):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': ['Falsche Anmeldedaten']}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request=request, username=user.username, password=password)
        if not user:
            return Response({'detail': ['Falsche Anmeldedaten']}, status=status.HTTP_400_BAD_REQUEST)
        data = {}
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }
        return Response(data, status=status.HTTP_200_OK)