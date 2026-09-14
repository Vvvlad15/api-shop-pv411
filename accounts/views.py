from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from main.models import Category  # Импортируем категории для корректной работы меню

def login_view(request):
    """Вхід у систему"""
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main:product_list')
    else:
        form = AuthenticationForm()
        
    context = {
        'form': form,
        'title': 'Авторизація',
        'categories': Category.objects.all()
    }
    return render(request, 'accounts/login.html', context)


def register_view(request):
    """Реєстрація нового користувача"""
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('main:product_list')
    else:
        form = UserCreationForm()

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
