from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import random
import string

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, UserForm
from users.services import send_new_password, send_register_email


class UserRegisterView(CreateView):
    """Представление для регистрации нового пользователя.

        Использует форму UserRegisterForm для создания пользователя.
        После успешной регистрации отправляет email с подтверждением регистрации.
        При успешном создании пользователя происходит редирект на страницу входа."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Создать аккаунт'
    }

    def form_valid(self, form):
        self.object = form.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
        Представление для входа пользователя в систему.

        Использует форму UserLoginForm.
        Шаблон отображает форму входа с заголовком.
        """

    form_class = UserLoginForm
    template_name = 'users/user_login.html'
    extra_context = {
        'title': "Вход в аккаунт"
    }


class UserProfileView(UpdateView):
    """
        Представление для просмотра профиля текущего пользователя в режиме только для чтения.

        Объект для редактирования — текущий пользователь.
        Контекст содержит заголовок с именем пользователя.
        """
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f"Ваш профиль {self.request.user}"
        return context_data


class UserUpdateView(UpdateView):
    """
        Представление для обновления данных профиля текущего пользователя.

        Использует форму UserForm.
        При успешном сохранении происходит редирект на страницу профиля.
        Контекст содержит заголовок с именем пользователя.
        """
    model = User
    form_class = UserForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f"Обновить профиль {self.request.user}"
        return context_data


class UserPasswordChangeView(PasswordChangeView):
    """
        Представление для изменения пароля текущего пользователя.

        Использует форму UserChangePasswordForm.
        При успешном изменении пароля происходит редирект на страницу профиля.
        Контекст содержит заголовок с именем пользователя.
        """
    form_class = UserChangePasswordForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f"Изменить пароль {self.request.user}"
        return context_data


class UserLogoutView(LogoutView):
    """
        Представление для выхода пользователя из системы.

        Отображает страницу выхода с заголовком.
        """
    template_name = 'users/user_logout.html'
    extra_context = {
        'title': 'Выход из аккаунта'
    }


class UserListView(LoginRequiredMixin, ListView):
    """
        Представление списка активных пользователей питомника.

        Доступно только аутентифицированным пользователям.
        Пагинация по 3 пользователя на страницу.
        Отображает только активных пользователей.
        Контекст содержит заголовок страницы.
        """
    model = User
    extra_context = {
        'title': "Питомник все наши пользователи"
    }
    template_name = 'users/users.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserDetailView(DetailView):
    """
        Представление подробного профиля пользователя по ID.

        Отображает данные выбранного пользователя.
        Контекст содержит заголовок с именем пользователя.
        """
    model = User
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user_obj = context_data['object']
        context_data['title'] = f"Профиль пользователя {user_obj}"
        return context_data


@login_required(login_url='users:user_login')
def user_generate_new_password_view(request):
    """
        Функция для генерации нового случайного пароля для текущего пользователя.

        Генерирует случайный пароль длиной 12 символов, меняет пароль пользователя,
        сохраняет изменения и отправляет новый пароль на email пользователя.
        После этого происходит редирект на главную страницу сайта.
        """
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
