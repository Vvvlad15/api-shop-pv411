from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Product, Category

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
