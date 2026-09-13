from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Модель категорії товарів"""
    name = models.CharField(max_length=50, db_index=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Слаг для URL")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])


class Product(models.Model):
    """Модель товару для інтернет-магазину"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категорія")
    name = models.CharField(max_length=255, verbose_name="Назва товару")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг для URL")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    stock = models.PositiveIntegerField(default=0, verbose_name="Кількість на складі")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name="Зображення")
    views = models.IntegerField(default=0, verbose_name="Кількість переглядів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    is_active = models.BooleanField(default=True, verbose_name="Активний")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Створено: {self.created_at.strftime('%d.%m.%Y')})"

    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])
