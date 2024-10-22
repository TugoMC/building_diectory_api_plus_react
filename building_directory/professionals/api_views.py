from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Professional, Contract, Review, Portfolio
from .serializers import ProfessionalSerializer, ContractSerializer, ReviewSerializer, PortfolioSerializer
from django.utils import timezone
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def filter(self, request):
        professionals = self.get_queryset()
        name_filter = request.query_params.get('name', '')
        specialization_filter = request.query_params.get('specialization', '')
        min_rating = request.query_params.get('min_rating')

        if name_filter:
            professionals = professionals.filter(full_name__icontains=name_filter)
        if specialization_filter:
            professionals = professionals.filter(specialization__icontains=specialization_filter)
        if min_rating:
            professionals = professionals.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=float(min_rating))

        serializer = self.get_serializer(professionals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def portfolios(self, request, pk=None):
        professional = self.get_object()
        portfolios = professional.portfolios.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        professional = self.get_object()
        is_available = professional.is_available()
        return Response({"is_available": is_available})

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contract.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        contract = self.get_object()
        contract.delete()
        return Response({"status": "contract cancelled"})

    @action(detail=True, methods=['post'])
    def initiate_payment(self, request, pk=None):
        contract = self.get_object()
        if contract.is_paid():
            return Response({"error": "This contract has already been paid."}, status=status.HTTP_400_BAD_REQUEST)

        total_days = (contract.end_date - contract.start_date).days + 1
        total_amount = int(contract.professional.daily_rate * total_days * 100)  # In cents

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Contract with {contract.professional.full_name}",
                        },
                        "unit_amount": total_amount,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=request.build_absolute_uri(f"/api/contracts/{contract.id}/payment_success/"),
                cancel_url=request.build_absolute_uri(f"/api/contracts/{contract.id}/payment_cancel/"),
            )
            return Response({"session_id": session.id, "total_amount": total_amount / 100})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def payment_success(self, request, pk=None):
        contract = self.get_object()
        if not contract.is_paid():
            contract.payment_status = "paid"
            contract.status = "confirmed"
            contract.save()
            contract.professional.is_available = False
            contract.professional.save()
        return Response({"status": "payment successful, contract confirmed"})

    @action(detail=True, methods=['post'])
    def payment_cancel(self, request, pk=None):
        return Response({"status": "payment cancelled"})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def submit_review(self, request):
        contract_id = request.data.get('contract_id')
        contract = get_object_or_404(Contract, id=contract_id, user=request.user)
        review, created = Review.objects.get_or_create(user=request.user, contract=contract, professional=contract.professional)
        
        serializer = self.get_serializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            review = serializer.save()
            if not created:
                review.edit_count += 1
                review.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    @action(detail=True, methods=['get'])
    def professional(self, request, pk=None):
        portfolio = self.get_object()
        serializer = ProfessionalSerializer(portfolio.professional)
        return Response(serializer.data)