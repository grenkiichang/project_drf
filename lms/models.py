# lms/models.py

from django.db import models
from django.conf import settings


class Course(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название курса')

    preview = models.ImageField(
        upload_to='course_previews/',
        blank=True,
        null=True,
        verbose_name='Превью курса'
    )
    description = models.TextField(verbose_name='Описание курса')


    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец курса'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    title = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(
        upload_to='lesson_previews/',
        blank=True,
        null=True,
        verbose_name='Превью урока'
    )
    video_link = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на видео'
    )


    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец урока'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.user} подписан на {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')