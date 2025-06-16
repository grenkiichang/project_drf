from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, PaymentViewSet # Убедись, что эти импорты верны
from django.urls import path, include


app_name = 'users' # Это для уникальности имен URL-ов

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment') # Если PaymentViewSet относится к users


urlpatterns = [
    path('', include(router.urls)),
]