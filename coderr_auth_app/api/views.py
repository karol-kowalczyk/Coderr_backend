from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from coderr_app.models import User
from .serializers import UserSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):



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