from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ParentCategory(models.Model):
    """
    Модель для главных категорий
    """
    name = models.CharField(
        'Название главной категории',
        max_length=255
    )

    class Meta:
        verbose_name = 'главная категория'
        verbose_name_plural = 'Главные категории'

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель для подкатегорий
    """
    name = models.CharField(
        'Название подкатегории',
        max_length=255
    )
    parent = models.ForeignKey(
        ParentCategory,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Название главной категории'
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель для товаров
    """
    name = models.CharField(
        'Название товара',
        max_length=255
    )
    description = models.TextField(
        'Описание товара',
    )
    price = models.DecimalField(
        'Цена товара',
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(
        'Количество товара на складе',
    )
    image = models.ImageField(
        'Фото товара',
        upload_to='products/'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Название подкатегории'
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Модель для корзины, связанной с пользователем.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'корзина пользователя'
        verbose_name_plural = 'Корзины пользователя'

    def __str__(self):
        return f'Корзина пользователя: {self.user.username}'


class CartItem(models.Model):
    """
    Модель для корзины, который содержит продукт и его количество.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        'Количество товара',
        default=0
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'
