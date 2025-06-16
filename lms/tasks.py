from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_lesson_creation_email(lesson_title, recipient_email):
    """
    Celery задача для отправки email оповещения о создании нового урока.
    """
    subject = f'Новый урок создан: {lesson_title}'
    message = f'Привет!\n\nТолько что был создан новый урок: "{lesson_title}".\n\nПриятного обучения!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    print(f"Email for lesson '{lesson_title}' sent to {recipient_email}")