from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

User = get_user_model()

# 1. Адаптируем форму регистрации под кастомного пользователя
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email") # Добавляем email к регистрации по стандарту


# 2. Адаптируем форму входа под кастомного пользователя
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User


# Формы для редактирования профиля (остаются без изменений)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Email-адреса',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date', 'location', 'website']
        labels = {
            'avatar': 'Аватар (зображення)',
            'bio': 'Про себе',
            'birth_date': 'Дата народження',
            'location': 'Місто',
            'website': 'Веб-сайт',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['birth_date', 'bio']:
                field.widget.attrs.update({'class': 'form-input'})
