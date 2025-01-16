from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .models import Cart, CartItem, Category, ParentCategory, Product


class BaseView:
    """
    Базовый класс для представлений,
    содержащий общие методы для работы с корзиной.
    """

    def get_cart(self):
        """
        Получает корзину текущего пользователя.

        Если пользователь аутентифицирован, возвращает корзину,
        связанную с пользователем.

        Если корзина не существует, создаёт новую.
        """
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            return cart
        return None

    def get_cart_quantity(self):
        """
        Подсчитывает общее количество товаров в корзине текущего пользователя.
        """
        cart = self.get_cart()
        return cart.items.aggregate(
            Sum('quantity'))['quantity__sum'] or 0 if cart else 0

    def get_cart_total_price(self):
        """
        Подсчитывает общую стоимость товаров в корзине текущего пользователя.
        """
        cart = self.get_cart()
        if cart:
            return round(
                sum(
                    item.quantity * item.product.price
                    for item in cart.items.all()
                ), 2
            )
        return 0.0

    def add_cart_quantity_to_context(self, context):
        """
        Добавляет общее количество товаров в корзине в указанный контекст.
        """
        context['total_quantity'] = self.get_cart_quantity()
        context['total_price'] = self.get_cart_total_price()
        context['category_list'] = ParentCategory.objects.prefetch_related(
            'subcategories').all()


class CategoryListView(BaseView, ListView):
    """
    Вывод списка главных категорий и подкатегорий.
    """
    model = ParentCategory
    template_name = 'shop/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return ParentCategory.objects.prefetch_related('subcategories').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.add_cart_quantity_to_context(context)
        return context


class ProductListView(BaseView, ListView):
    """
    Вывод списка товаров.
    """
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'product_list'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        queryset = Product.objects.filter(
            category__id=category_id).select_related('category')

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, id=self.kwargs.get('category_id'))
        context['search_query'] = self.request.GET.get('search', '')
        self.add_cart_quantity_to_context(context)
        return context


class ProductDetailView(BaseView, DetailView):
    """
    Вывод для отображения конкретного товара.
    """
    model = Product
    template_name = 'shop/product_detail.html'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('product_id')
        return get_object_or_404(Product, id=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.add_cart_quantity_to_context(context)
        return context


class CartCreateView(BaseView, LoginRequiredMixin, CreateView):
    """
    Добавляет продукт в корзину.
    Если продукт уже есть в корзине, увеличивает его количество.
    """
    model = CartItem

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart()

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer) if referer else redirect('shop:view_cart')


class CartIncreaseView(BaseView, LoginRequiredMixin, View):
    """
    View для увеличения количества товара в корзине.
    """

    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            'success': True,
            'new_quantity': cart_item.quantity,
            'total_quantity': self.get_cart_quantity(),
            'total_price': self.get_cart_total_price(),
            'product_price': cart_item.product.price,
            'item_total': round(
                cart_item.quantity * cart_item.product.price, 2)
        })


class CartDecreaseView(BaseView, LoginRequiredMixin, View):
    """
    View для уменьшения количества товара в корзине.
    """

    def post(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem, id=item_id, cart__user=self.request.user)
        new_quantity = cart_item.quantity - 1

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            item_total = round(cart_item.quantity * cart_item.product.price, 2)
        else:
            cart_item.delete()
            item_total = 0
            new_quantity = 0

        return JsonResponse({
            'success': True,
            'new_quantity': new_quantity,
            'total_quantity': self.get_cart_quantity(),
            'total_price': self.get_cart_total_price(),
            'product_price': cart_item.product.price,
            'item_total': item_total
        })


class CartListView(BaseView, LoginRequiredMixin, ListView):
    """
    Отображает содержимое корзины для авторизованного пользователя.
    """
    model = CartItem
    template_name = 'shop/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = self.get_cart()
        return cart.items.all() if cart else CartItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.add_cart_quantity_to_context(context)

        context['cart_items_with_total_price'] = [
            {
                'item': item,
                'total_price': item.product.price * item.quantity
            }
            for item in context['cart_items']
        ]
        return context


class CartItemDeleteView(BaseView, LoginRequiredMixin, DeleteView):
    """
    Удаляет товар из корзины.
    """
    model = CartItem
    template_name = 'shop/cart.html'

    def get_queryset(self):
        return super().get_queryset().filter(cart__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return JsonResponse({
            'success': True,
            'total_quantity': self.get_cart_quantity(),
            'total_price': self.get_cart_total_price(),
        })


class ClearCartView(BaseView, LoginRequiredMixin, View):
    """
    Очищает корзину пользователя.
    """

    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        if cart:
            cart.items.all().delete()
        return redirect('shop:view_cart')


def page_not_found(request, exception):
    """
    Обрабатывает ошибки 404 Not Found.
    """
    return render(request,
                  'shop/404.html',
                  status=HTTPStatus.NOT_FOUND
                  )


def csrf_failure(request, reason=''):
    """
    Обрабатывает сбои проверки токена CSRF.
    """
    return render(request,
                  'shop/403csrf.html',
                  status=HTTPStatus.FORBIDDEN
                  )


def server_error(request):
    """
    Обрабатывает ошибки 500 Internal Server Error.
    """
    return render(request,
                  'shop/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR
                  )


def permission_denied(request, exception):
    """
    Обрабатывает ошибки 403 Forbidden.
    """
    return render(request,
                  'shop/403csrf.html',
                  status=HTTPStatus.FORBIDDEN
                  )
