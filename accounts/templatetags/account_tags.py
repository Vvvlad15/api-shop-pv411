from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def days_on_site(date_joined):
    """Обчислює кількість днів на сайті та правильно відмінює слово 'день'"""
    delta = timezone.now() - date_joined
    days = delta.days

    if days <= 0:
        return "перший день"

    # Проверка на исключения: 11, 12, 13, 14 днів
    last_two_digits = days % 100
    if last_two_digits >= 11 and last_two_digits <= 14:
        return f"{days} днів"
    
    # Проверка по последней цифре
    remainder = days % 10
    if remainder == 1:
        return f"{days} день"
    elif remainder >= 2 and remainder <= 4:
        return f"{days} дні"
    else:
        return f"{days} днів"
