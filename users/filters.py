# users/filters.py

import django_filters
from users.models import Payment
from django_filters import DateFromToRangeFilter # Для фильтрации по диапазону дат

class PaymentFilter(django_filters.FilterSet):
    # Фильтр по дате оплаты (диапазон от-до)
    # Позволяет запросы типа ?payment_date_after=2025-01-01&payment_date_before=2025-06-30
    payment_date = DateFromToRangeFilter()

    # Фильтр по оплаченному курсу (используется id курса)
    paid_course = django_filters.ModelChoiceFilter(queryset=Payment.objects.all().values_list('paid_course', flat=True).distinct(), field_name='paid_course__id')

    # Фильтр по оплаченному уроку (используется id урока)
    paid_lesson = django_filters.ModelChoiceFilter(queryset=Payment.objects.all().values_list('paid_lesson', flat=True).distinct(), field_name='paid_lesson__id')

    # Фильтр по способу оплаты (cash/transfer)
    payment_method = django_filters.ChoiceFilter(choices=Payment.METHOD_CHOICES)

    # Фильтр для сортировки (ordering)
    # Позволяет запросы типа ?ordering=-payment_date (для убывания) или ?ordering=payment_date (для возрастания)
    # Можете добавить другие поля для сортировки, например, 'payment_amount'
    ordering = django_filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
            ('payment_amount', 'payment_amount'),
        ),
        choices=(
            ('payment_date', 'Дата оплаты (по возрастанию)'),
            ('-payment_date', 'Дата оплаты (по убыванию)'),
            ('payment_amount', 'Сумма оплаты (по возрастанию)'),
            ('-payment_amount', 'Сумма оплаты (по убыванию)'),
        )
    )

    class Meta:
        model = Payment
        fields = ['payment_date', 'paid_course', 'paid_lesson', 'payment_method', 'ordering']