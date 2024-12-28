from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from .models import Cart, CartItem, ParentCategory, Product


class CategoryListView(ListView):
    """
    Вывод списка главных категорий и подкатегорий
    """
    model = ParentCategory
    template_name = 'shop/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return ParentCategory.objects.prefetch_related('subcategories').all()


class ProductListView(ListView):
    """
    Вывод списка товаров
    """
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'product_list'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category__id=category_id)


class ProductDetailView(DetailView):
    """
    Вывод для отображения конкретного товара
    """
    model = Product
    template_name = 'shop/product_detail.html'


class CartCreateView(LoginRequiredMixin, CreateView):
    """
    Добавляет продукт в корзину.
    Если продукт уже есть в корзине, увеличивает его количество.
    """
    model = CartItem
    template_name = 'shop/cart.html'

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')


class CartListView(LoginRequiredMixin, ListView):
    """
    Отображает содержимое корзины для авторизованного пользователя.
    """
    model = CartItem
    template_name = 'shop/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return cart.items.all()


def page_not_found(request, exception):
    """
    Обрабатывает ошибки 404 Not Found.
    """
    return render(
        request,
        'shop/404.html',
        status=HTTPStatus.NOT_FOUND
    )


def csrf_failure(request, reason=''):
    """
    Обрабатывает сбои проверки токена CSRF.
    """
    return render(
        request,
        'shop/403csrf.html',
        status=HTTPStatus.FORBIDDEN
    )


def server_error(request):
    """
    Обрабатывает ошибки 500 Internal Server Error.
    """
    return render(
        request,
        'shop/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


def permission_denied(request, exception):
    """
    Обрабатывает ошибки 403 Forbidden.
    """
    return render(
        request,
        'shop/403csrf.html',
        status=HTTPStatus.FORBIDDEN
    )
