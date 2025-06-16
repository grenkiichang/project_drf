# lms/serializers.py

from rest_framework import serializers
from lms.models import Course, Lesson
from .validators import validate_youtube_link
from lms.models import Subscription

class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    """
    Сериализатор для модели Lesson.
    Преобразует объекты Lesson в формат JSON и обратно.
    """
    class Meta:
        model = Lesson
        fields = '__all__'

        extra_kwargs = {
            'video_link': {'validators': [validate_youtube_link]},
        }

    def validate(self, data):
        forbidden_words = ['фарфор', 'керамика']

        if 'title' in data and data['title']:
            title_lower = data['title'].lower()
            for word in forbidden_words:
                if word in title_lower:
                    raise serializers.ValidationError(
                        f"Слово '{word}' запрещено в названии урока."
                    )

        if 'description' in data and data['description']:
            description_lower = data['description'].lower()
            for word in forbidden_words:
                if word in description_lower:
                    raise serializers.ValidationError(
                        f"Слово '{word}' запрещено в описании урока."
                    )
        return data


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')

    lessons = LessonSerializer(many=True, read_only=True)

    is_subscribed = serializers.SerializerMethodField()
    """
    Сериализатор для модели Course.
    Преобразует объекты Course в формат JSON и обратно.
    """
    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')  # Получаем объект запроса из контекста сериализатора
        if request and request.user.is_authenticated:  # Проверяем, что пользователь аутентифицирован
            # Проверяем наличие подписки для текущего курса и пользователя
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False  # Если пользователь не аутентифицирован, считаем, что не подписан


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'