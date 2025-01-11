# views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User


class UserProfileCreateView(APIView):
    """
    Diese View ermöglicht es, einen neuen Benutzer mit einem Benutzerprofil zu erstellen.
    """

    def post(self, request, *args, **kwargs):
        # Serialisieren der Eingabedaten aus der Anfrage
        serializer = UserProfileSerializer(data=request.data)

        # Validierung der Eingabedaten
        if serializer.is_valid():
            # Benutzer und Profil erstellen, falls die Validierung erfolgreich ist
            user_profile = serializer.save()

            # Erfolgreiche Registrierung: Status 201 Created
            response_data = {
                "username": user_profile.user.username,
                "email": user_profile.user.email,
                "role": user_profile.role
            }

            # Gibt die Antwort mit dem Status 201 Created zurück
            return Response(response_data, status=status.HTTP_201_CREATED)

        # Wenn die Validierung fehlschlägt, gibt die Fehler mit Status 400 Bad Request zurück
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    pass