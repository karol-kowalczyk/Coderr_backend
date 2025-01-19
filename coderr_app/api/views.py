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


class ReviewsFilter(django_filters.FilterSet):

    business_user_id = django_filters.NumberFilter(field_name='business_user__id')
    reviewer_id = django_filters.NumberFilter(field_name='customer_user__id')

    class Meta:
        model = Reviews
        fields = ['business_user_id', 'reviewer_id']


class ReviewsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsReviewerOrAdminPermission]
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewsFilter
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def perform_create(self, serializer):

        serializer.save(customer_user=self.request.user)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BaseInfoView(generics.ListAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfile

    def _calculate_average_rating(self):

        ratings = Reviews.objects.values_list('rating', flat=True)
        total_ratings = ratings.count()
        if total_ratings == 0:
            return 0
        
        return round(sum(ratings) / total_ratings, 1)

    def list(self, request):

        business_profile_count = UserProfile.objects.filter(type='business').count()
        review_count = Reviews.objects.count()
        offer_count = Offers.objects.count()
        average_rating = self._calculate_average_rating()

        return Response({
            'business_profile_count': business_profile_count,
            'review_count': review_count,
            'offer_count': offer_count,
            'average_rating': average_rating
        })

class OrdersViewSet(viewsets.ModelViewSet):

    permission_classes = [OrderAccessPermission]
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()

    def get_queryset(self):

        user = self.request.user
        if user.user_profile.type == 'staff':
            return Orders.objects.all()
        else:
            customer_orders = Orders.objects.filter(customer_user=user)
            business_orders = Orders.objects.filter(business_user=user)
            return customer_orders | business_orders

    def perform_create(self, serializer):

        offer_detail_id = self.request.data.get('offer_detail_id')

        try:
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
            offer = offer_detail.offer
            customer_user = self.request.user
            business_user = offer.user

            serializer.save(
                customer_user=customer_user,
                business_user=business_user,
                offer=offer,
                offer_details=offer_detail,
                title=offer.title,
                revisions=offer_detail.revisions,
                delivery_time_in_days=offer_detail.delivery_time_in_days,
                price=offer_detail.price,
                features=offer_detail.features,
                offer_type=offer_detail.offer_type,
                status='in_progress'
            )

        except OfferDetails.DoesNotExist:
            raise ValueError('Invalid offer_detail_id')
        
    def create(self, request, *args, **kwargs):

        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)