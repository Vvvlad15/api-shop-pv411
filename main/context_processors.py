from .cart import Cart

def cart(request):
    """Глобальний контекстний процесор кошика для всього сайту"""
    return {'cart': Cart(request)}
