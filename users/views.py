from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
import random
import string

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, UserForm
from users.services import send_new_password, send_register_email


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Создать аккаунт'
    }


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/user_login.html'
    extra_context = {
        'title': "Вход в аккаунт"
    }


class UserProfileView(UpdateView):
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
    form_class = UserChangePasswordForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f"Изменить пароль {self.request.user}"
        return context_data


# @login_required(login_url='users:user_login')
# def user_change_password_view(request):
#     user_object = request.user
#     form = UserChangePasswordForm(user_object, request.POST)
#     if request.method == "POST":
#         if form.is_valid():
#             user_object = form.save()
#             update_session_auth_hash(request, user_object)
#             messages.success(request, 'Пароль был успешно изменен!')
#             return HttpResponseRedirect(reverse('users:user_profile'))
#         else:
#             messages.error(request, 'Не удалось изменить пароль')
#     context = {
#         'title': f"Изменить пароль {user_object.first_name} {user_object.last_name}",
#         'form': form
#     }
#     return render(request, 'users/user_change_password.html', context=context)


@login_required(login_url='users:user_login')
def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')


@login_required(login_url='users:user_login')
def user_generate_new_password_view(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))