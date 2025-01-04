from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView

from shop.views import BaseView
from users.forms import ProfileCreateUpdateForm

User = get_user_model()


class ProfileCreateView(CreateView):
    """
    Создание пользователя
    """
    model = User
    form_class = ProfileCreateUpdateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class ProfileDetailView(LoginRequiredMixin, DetailView, BaseView):
    """
    Просмотр профиля пользователя
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.add_cart_quantity_to_context(context)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView, BaseView):
    """
    Редактирование профиля, требующее логина.
    """
    model = User
    form_class = ProfileCreateUpdateForm
    template_name = 'users/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super(ProfileUpdateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('users:profile',
                            kwargs={'username': self.request.user.username})
