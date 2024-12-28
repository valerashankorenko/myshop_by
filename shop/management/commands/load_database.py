import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from shop.models import Category, ParentCategory, Product

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загрузка пользователей, категорий и товаров в базу'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Загрузка пользователей, категорий и товаров в базу начата'))

        self.load_users()
        self.load_parent_categories()
        self.load_categories()
        self.load_products()

        self.stdout.write(self.style.SUCCESS('Данные загружены'))

    def load_users(self):
        try:
            with open('data/users.json', encoding='utf-8') as data_file_users:
                user_data = json.load(data_file_users)
                for user in user_data:
                    user_password = make_password(
                        user['password'])  # Хэшируем пароль
                    try:
                        User.objects.get_or_create(
                            username=user['username'],
                            defaults={
                                'email': user['email'],
                                'password': user_password,
                                'phone_number': user.get('phone_number'),
                                'first_name': user.get('first_name'),
                                'last_name': user.get('last_name')
                            }
                        )
                    except IntegrityError:
                        self.stdout.write(self.style.ERROR(
                            f"Пользователь {user['username']} уже существует."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл users.json не найден.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке пользователей: {str(e)}'))

    def load_parent_categories(self):
        try:
            with open(
                'data/parent_categories.json', encoding='utf-8'
            ) as data_file_parent_categories:
                parent_categories_data = json.load(data_file_parent_categories)
                for parent in parent_categories_data:
                    ParentCategory.objects.get_or_create(**parent)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                'Файл parent_categories.json не найден.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке родительских категорий: {str(e)}'))

    def load_categories(self):
        try:
            with open(
                'data/categories.json', encoding='utf-8'
            ) as data_file_categories:
                categories_data = json.load(data_file_categories)
                for category in categories_data:
                    Category.objects.get_or_create(**category)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                'Файл categories.json не найден.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке категорий: {str(e)}'))

    def load_products(self):
        try:
            with open(
                'data/product.json', encoding='utf-8'
            ) as data_file_product:
                product_data = json.load(data_file_product)
                for product in product_data:
                    category_id = product.pop('category', None)
                    if category_id is not None:
                        try:
                            category = Category.objects.get(id=category_id)
                            product['category'] = category
                            Product.objects.get_or_create(**product)
                        except Category.DoesNotExist:
                            self.stdout.write(self.style.ERROR(
                                f'Категория с ID {category_id} не найдена'
                                f'для товара {product["name"]}.'))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'Не указана категория '
                            f'для товара {product["name"]}.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл product.json не найден.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке продуктов: {str(e)}'))
