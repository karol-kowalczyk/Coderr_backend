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
    
class CompletedOrderCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):

        if not User.objects.filter(id=business_user_id, user_profile__type='business').exists():
            return Response({'error': 'Business user not found.'}, status.HTTP_400_BAD_REQUEST)

        completed_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()

        return Response({'completed_order_count': completed_count})

    
class BusinessProfilesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):

        return UserProfile.objects.filter(type='business')
    

class CustomerProfilesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileDetailSerializer

    def get_queryset(self):

        return UserProfile.objects.filter(type='customer')
    

class OfferFilter(django_filters.FilterSet):


    class Meta:
        model = Offers
        fields = ['max_delivery_time', 'creator_id']

    def filter_by_max_delivery_time(self, queryset, name, value):

        return queryset.filter(max_delivery_time__lte=value)
     

class OffersViewSet(viewsets.ModelViewSet):

    permission_classes = [IsBusinessOrAdminPermission]
    serializer_class = OffersSerializer
    queryset = Offers.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['min_price', 'created_at', 'max_delivery_time']
    ordering = ['created_at']
    search_fields = ['title', 'description']

    def get_serializer_context(self):

        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):

        min_price_subquery = OfferDetails.objects.filter(offer=OuterRef('pk')).values('offer').annotate(
            min_price=Min('price')
        ).values('min_price')

        min_delivery_time_subquery = OfferDetails.objects.filter(offer=OuterRef('pk')).values('offer').annotate(
            min_delivery_time=Min('delivery_time_in_days')
        ).values('min_delivery_time')

        return Offers.objects.annotate(
            min_price=Subquery(min_price_subquery),
            min_delivery_time=Subquery(min_delivery_time_subquery),
            max_delivery_time=Subquery(min_delivery_time_subquery)
        )

