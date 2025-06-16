# lms/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet, LessonViewSet, SubscriptionAPIView

app_name = 'lms'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    # Включаем маршруты, сгенерированные роутером
    *router.urls,

    # Если SubscriptionAPIView не часть роутера и имеет свой собственный path:
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription_toggle'),
]