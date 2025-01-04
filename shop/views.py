from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .models import Cart, CartItem, Category, ParentCategory, Product


class CategoryListView(ListView):
    """
    Вывод списка главных категорий и подкатегорий
    """
    model = ParentCategory
    template_name = 'shop/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return ParentCategory.objects.prefetch_related('subcategories').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['total_quantity'] = cart.items.aggregate(Sum('quantity'))[
                'quantity__sum'] or 0
        else:
            context['total_quantity'] = 0
        return context


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
        return Product.objects.filter(
            category__id=category_id).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['total_quantity'] = cart.items.aggregate(Sum('quantity'))[
                'quantity__sum'] or 0
        else:
            context['total_quantity'] = 0
        return context


class ProductDetailView(DetailView):
    """
    Вывод для отображения конкретного товара
    """
    model = Product
    template_name = 'shop/product_detail.html'

    def get_object(self, queryset=None):
        return self.get_queryset().get(id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['total_quantity'] = cart.items.aggregate(Sum('quantity'))[
                'quantity__sum'] or 0
        else:
            context['total_quantity'] = 0
        return context


class CartCreateView(LoginRequiredMixin, CreateView):
    """
    Добавляет продукт в корзину.
    Если продукт уже есть в корзине, увеличивает его количество.
    """
    model = CartItem

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if created:
            # Если товар был создан, устанавливаем количество на 1
            cart_item.quantity = 1
        else:
            # Если товар уже существует, увеличиваем количество на 1
            cart_item.quantity += 1

        cart_item.save()

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('shop:view_cart')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        context['total_quantity'] = cart.items.aggregate(Sum('quantity'))[
            'quantity__sum'] or 0
        total_price = cart.items.aggregate(Sum('product__price'))[
            'product__price__sum'] or 0
        context['total_price'] = round(total_price, 2)
        return context


class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаляет товар из корзины.
    """
    model = CartItem
    template_name = 'shop/cart.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(cart__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        cart_items = self.get_queryset()
        total_quantity = cart_items.count()
        total_price = sum(
            item.product.price * item.quantity for item in cart_items
        )

        return JsonResponse({
            'success': True,
            'total_quantity': total_quantity,
            'total_price': total_price
        })


class ClearCartView(LoginRequiredMixin, View):
    """
    Очищает корзину пользователя.
    """

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return redirect('shop:view_cart')


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
