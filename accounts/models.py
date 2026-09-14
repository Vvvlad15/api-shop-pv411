from django.db import models
from django.conf import settings  # Подключаем настройки проекта
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Модель профілю користувача (One-to-One зв'язок з кастомною моделлю)"""
    # Вместо User используем settings.AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, verbose_name="Аватар")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    location = models.CharField(max_length=50, blank=True, verbose_name="Місто")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

    def __str__(self):
        return f"Профіль {self.user.username}"


# =================================================================
# ⚡ СИГНАЛИ (Автоматичне створення профілю)
# =================================================================

@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # Меняем sender на кастомную модель
def create_user_profile(sender, instance, created, **kwargs):
    """Створює профіль при реєстрації нового користувача"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # Меняем sender на кастомную модель
def save_user_profile(sender, instance, **kwargs):
    """Зберігає профіль при оновленні користувача"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
