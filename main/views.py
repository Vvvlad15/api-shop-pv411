from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from .models import Product, Category
from django.views.decorators.http import require_POST
from .cart import Cart

def product_list(request, category_slug=None):
    """Список товаров со встроенной сортировкой и оптимизацией запросов"""
    # select_related устраняет проблему N+1 запросов
    products = Product.objects.select_related('category').filter(is_active=True)
    categories = Category.objects.all()
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Получаем параметр сортировки из GET-запроса (по умолчанию 'new')
    sort = request.GET.get('sort', 'new')
    
    if sort == 'old':
        products = products.order_by('created_at')
    elif sort == 'popular':
        products = products.order_by('-views', '-created_at')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:  # 'new'
        products = products.order_by('-created_at')

    context = {
        "title": f"Категорія: {category.name}" if category else "Каталог товарів",
        "categories": categories,
        "category": category,
        "products": products,
        "current_sort": sort,
    }
    return render(request, "main/product_list.html", context)


def product_detail(request, id, slug):
    """Детальная страница товара с безопасным счетчиком просмотров F()"""
    product = get_object_or_404(
        Product.objects.select_related('category'),
        id=id,
        slug=slug,
        is_active=True
    )

    # Безопасное атомарное обновление счетчика в базе данных через выражение F()
    Product.objects.filter(id=id).update(views=F('views') + 1)
    
    # Обновляем данные в текущем объекте, чтобы вывести актуальное число в шаблон
    product.refresh_from_db(fields=['views'])

    # Выборка до 4 похожих товаров из той же категории, исключая текущий
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('category')[:4]

    context = {
        "title": product.name,
        "product": product,
        "related_products": related_products,
    }
    return render(request, "main/product_detail.html", context)
def contact_view(request):
    """Обробка форми зворотного зв'язку та надсилання email адміністратору"""
    categories = Category.objects.all() # для навігації у base.html
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Отримуємо очищені та безпечні дані з форми
            cd = form.cleaned_data
            
            # Формуємо красивий текст листа для адміна
            subject = f"Зворотний зв'язок: {cd['subject']}"
            message_body = (
                f"Отримано нове повідомлення з форми контактів.\n\n"
                f"Відправник: {cd['name']}\n"
                f"Email відправника: {cd['email']}\n\n"
                f"Текст повідомлення:\n{cd['message']}"
            )
            
            try:
                # Надсилаємо лист (відправник, отримувач)
                send_mail(
                    subject,
                    message_body,
                    cd['email'], # email користувача
                    ['admin@api-shop.com'], # email адміністратора сайту
                    fail_silently=False,
                )
                messages.success(request, "Ваше повідомлення успішно надіслано адміністратору!")
                return redirect('main:contact') # Патерн Post/Redirect/Get
                
            except Exception as e:
                # Обробка помилок поштового сервера
                messages.error(request, f"Виникла помилка при відправці листа: {e}")
    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'categories': categories,
        'title': 'Зворотний зв\'язок (Контакти)'
    }
    return render(request, 'main/contact.html', context)
@require_POST
def cart_add(request, product_id):
    """Додавання або оновлення кількості товару в кошику"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Отримуємо кількість з форми (за замовчуванням 1)
    quantity = int(request.POST.get('quantity', 1))
    # Перевіряємо, чи потрібно перезаписати кількість (наприклад, зсередини кошика)
    override = request.POST.get('override', 'False') == 'True'
    
    cart.add(product=product, quantity=quantity, override_quantity=override)
    return redirect('main:cart_detail')


def cart_remove(request, product_id):
    """Видалення позиції з кошика"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('main:cart_detail')


def cart_detail(request):
    """Відображення вмісту кошика"""
    categories = Category.objects.all()
    context = {
        'title': 'Ваш кошик покупок',
        'categories': categories,
    }
    return render(request, 'main/cart_detail.html', context)