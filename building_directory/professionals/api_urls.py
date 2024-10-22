from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProfessionalViewSet, ContractViewSet, ReviewViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r'professionals', ProfessionalViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'portfolios', PortfolioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]