# users/views.py
import django_filters
from rest_framework import viewsets
from users.models import Payment
from .serializers import PaymentSerializer, UserSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (OrderingFilter,)

    ordering_fields = ['payment_date', 'payment_amount']
    ordering = ['-payment_date']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
