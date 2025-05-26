from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (JobOfferViewSet, SavedOfferViewSet, UserViewSet,
                    register_user, login_user)

# Configurar el router
router = DefaultRouter()
router.register(r'jobs', JobOfferViewSet)
router.register(r'saved-jobs', SavedOfferViewSet, basename='saved-jobs')
router.register(r'users', UserViewSet, basename='users')

# URLs de la API
urlpatterns = [
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('', include(router.urls)),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]