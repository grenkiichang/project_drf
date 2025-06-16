from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User, Payment# Предполагаем, что модель User находится здесь
from lms.models import Course, Lesson # Модели из приложения lms

class Command(BaseCommand):
    help = 'Создает группу "Модераторы" и назначает ей необходимые права.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Проверяем и создаем группу "Модераторы"...'))

        # Получаем или создаем группу "Модераторы"
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" успешно создана.'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" уже существует.'))


        user_content_type = ContentType.objects.get_for_model(User)
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)
        payment_content_type = ContentType.objects.get_for_model(Payment)

        # users/management/commands/create_moderator_group.py



        permissions_to_add = [

            'users.view_user',

            'lms.view_course',
            'lms.add_lesson',
            'lms.change_lesson',
            'lms.delete_lesson',
            'lms.view_lesson',
            'lms.change_course',

            # Права на платежи (теперь из users.models, префикс 'users')
            'users.view_payment',
            'users.add_payment',
            'users.change_payment',


        ]

        # ... (код снизу)

        added_count = 0
        for perm_codename in permissions_to_add:
            try:
                app_label, codename = perm_codename.split('.')
                permission = Permission.objects.get(codename=codename, content_type__app_label=app_label)
                if permission not in moderator_group.permissions.all():
                    moderator_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Добавлено разрешение: {perm_codename}'))
                    added_count += 1
                else:
                    self.stdout.write(self.style.NOTICE(f'Разрешение {perm_codename} уже присутствует.'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Ошибка: Разрешение {perm_codename} не найдено. Возможно, не выполнены миграции для соответствующего приложения.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Непредвиденная ошибка при добавлении {perm_codename}: {e}'))


        self.stdout.write(self.style.SUCCESS(f'Операция завершена. Добавлено {added_count} новых разрешений.'))
        self.stdout.write(self.style.SUCCESS('Группа "Модераторы" готова.'))