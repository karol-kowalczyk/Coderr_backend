from rest_framework.views import APIView

class UserProfileDetailView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsObjectOwnerOrAdminPermission | IsCustomerReadOnlyPermission]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class OfferDetailsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailsSerializer
    queryset = OfferDetails.objects.all()




class InProgressOrderCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
      
        if not User.objects.filter(id=business_user_id, user_profile__type='business').exists():
            return Response({'error': 'Business user not found.'}, status.HTTP_400_BAD_REQUEST)

        in_progress_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        return Response({'order_count': in_progress_count})
    
