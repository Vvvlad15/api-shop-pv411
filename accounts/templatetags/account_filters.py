from django import template

register = template.Library()

@register.filter(name='user_role')
def user_role(user):
    """Повертає текстову роль користувача на основі його статусу"""
    if user.is_staff:
        return "Адміністратор"
    return "Користувач"
