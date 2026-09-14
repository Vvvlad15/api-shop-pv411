from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Category

# Подключаем ВСЕ наши формы из файла forms.py
from .forms import (
    UserEditForm, 
    ProfileEditForm, 
    CustomUserCreationForm, 
    CustomAuthenticationForm
)

def login_view(request):
    """Вхід у систему з підтримкою кастомного User"""
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main:product_list')
    else:
        form = CustomAuthenticationForm()
        
    context = {
        'form': form,
        'title': 'Авторизація',
        'categories': Category.objects.all()
    }
    return render(request, 'accounts/login.html', context)


def register_view(request):
    """Реєстрація нового користувача з підтримкою кастомного User"""
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:product_list')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'title': 'Реєстрація',
        'categories': Category.objects.all()
    }
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    """Вихід із системи"""
    logout(request)
    return redirect('main:product_list')


@login_required
def profile_view(request):
    """Особистий кабінет (Профіль)"""
    context = {
        'title': f'Профіль {request.user.username}',
        'categories': Category.objects.all()
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """Редагування даних користувача та профілю"""
    categories = Category.objects.all()
    
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профіль успішно оновлено!")
            return redirect('accounts:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'categories': categories,
        'title': 'Редагування профілю'
    }
    return render(request, 'accounts/profile_edit.html', context)
