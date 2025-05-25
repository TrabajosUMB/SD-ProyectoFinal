from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet, SavedOfferViewSet

# Configurar el router
router = DefaultRouter()
router.register(r'jobs', JobOfferViewSet)
router.register(r'saved-jobs', SavedOfferViewSet, basename='saved-jobs')

# URLs de la API
urlpatterns = router.urls