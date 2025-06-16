# lms/views.py (ДОЛЖЕН ВЫГЛЯДЕТЬ ТАК)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from lms.models import Course, Subscription
from .tasks import send_lesson_creation_email


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        # Сохраняем урок, как обычно
        lesson = serializer.save(owner=self.request.user)

        # Получаем email пользователя, создавшего урок (или любого другого получателя)
        recipient_email = self.request.user.email

        # Вызываем Celery-задачу для отправки письма асинхронно
        send_lesson_creation_email.delay(lesson.title, recipient_email)
        print(f"Задача отправки email для урока '{lesson.title}' поставлена в очередь для {recipient_email}")

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated] # Только авторизованные пользователи могут управлять подписками

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"message": "Необходимо указать 'course_id'."}, status=400)

        # Получаем объект курса, или 404, если не найден
        course_item = get_object_or_404(Course, pk=course_id)

        # Ищем подписку по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена.'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена.'

        # Возвращаем ответ в API
        return Response({"message": message}, status=200)
