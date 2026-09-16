from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        """Ініціалізація кошика із сесії користувача"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Якщо кошика немає в сесії, створюємо порожній
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Додавання товару до кошика або оновлення його кількості"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price) # Decimal конвертуємо в рядок для JSON
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Позначення сесії як зміненої для збереження в БД/кеш"""
        self.session.modified = True

    def remove(self, product):
        """Видалення товару з кошика"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебір елементів кошика та підтягування об'єктів Product з бази"""
        product_ids = self.cart.keys()
        # Отримуємо об'єкти товарів прямо з БД
        products = Product.objects.filter(id__in=product_ids)
        
        cart_copy = self.cart.copy()
        for product in products:
            cart_copy[str(product.id)]['product'] = product

        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Підрахунок загальної кількості всіх одиниць товарів у кошику"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Підрахунок загальної вартості всього кошика"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очищення кошика із сесії"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
