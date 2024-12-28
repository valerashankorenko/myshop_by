from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Cart, CartItem, Category, ParentCategory, Product

User = get_user_model()


class ParentCategoryModelTestCase(TestCase):
    def test_create_parent_category(self):
        """Тест создания главной категории."""
        parent_category = ParentCategory.objects.create(name='Электроника')
        self.assertEqual(parent_category.name, 'Электроника')


class CategoryModelTestCase(TestCase):
    def test_create_category(self):
        """Тест создания подкатегории."""
        parent_category = ParentCategory.objects.create(name='Электроника')
        category = Category.objects.create(
            name='Смартфоны', parent=parent_category)
        self.assertEqual(category.name, 'Смартфоны')
        self.assertEqual(category.parent, parent_category)


class ProductModelTestCase(TestCase):
    def test_create_product(self):
        """Тест создания товара."""
        parent_category = ParentCategory.objects.create(name='Электроника')
        category = Category.objects.create(
            name='Смартфоны', parent=parent_category)
        product = Product.objects.create(
            name='iPhone 13',
            description='Описание iPhone 13',
            price=999.99,
            stock=50,
            category=category
        )
        self.assertEqual(product.name, 'iPhone 13')
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.stock, 50)
        self.assertEqual(product.category, category)


class CartModelTestCase(TestCase):
    def test_create_cart(self):
        """Тест создания корзины для пользователя."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Петя',
            last_name='Иванов',
            phone_number='+37529111111',
            password='testpassword'
        )
        cart = Cart.objects.create(user=user)
        self.assertEqual(cart.user, user)


class CartItemModelTestCase(TestCase):
    def test_create_cart_item(self):
        """Тест создания элемента корзины."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Петя',
            last_name='Иванов',
            phone_number='+37529111111',
            password='testpassword'
        )
        cart = Cart.objects.create(user=user)
        parent_category = ParentCategory.objects.create(name='Электроника')
        category = Category.objects.create(
            name='Смартфоны', parent=parent_category)
        product = Product.objects.create(
            name='iPhone 13',
            description='Описание iPhone 13',
            price=999.99,
            stock=50,
            category=category
        )
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=2)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.quantity, 2)
