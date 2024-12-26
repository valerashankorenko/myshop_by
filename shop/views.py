from http import HTTPStatus
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem, Category, Product


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})


def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    """
    Добавляет продукт в корзину. Если продукт уже есть в корзине, увеличивает его количество.

    :param request: HTTP запрос.
    :param product_id: ID продукта, который нужно добавить в корзину.
    :return: Редирект на страницу продукта.
    """
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product_detail', product_id=product.id)

@login_required
def view_cart(request):
    """
    Отображает содержимое корзины для авторизованного пользователя.

    :param request: HTTP запрос.
    :return: Рендерит шаблон корзины с её содержимым.
    """
    cart = Cart.objects.get(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})


def page_not_found(request, exception):
    """
    Обрабатывает ошибки 404 Not Found.
    """
    return render(request,
                  'shop/404.html',
                  status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    """
    Обрабатывает сбои проверки токена CSRF.
    """
    return render(request,
                  'shop/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)


def server_error(request):
    """
    Обрабатывает ошибки 500 Internal Server Error.
    """
    return render(request,
                  'shop/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    """
    Обрабатывает ошибки 403 Forbidden.
    """
    return render(request,
                  'shop/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)
