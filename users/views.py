from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.forms import UserRegisterForm, UserLoginForm


def user_register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            print(form.cleaned_data['password'])
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('users:user_login'))
    context = {
        'title': 'Создать аккаунт',
        'form': UserRegisterForm
    }
    return render(request, 'users/user_register.html', context=context)

def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dogs:index'))
            return HttpResponse("Вы не зарегистрированы либо неверный пароль, либо вы забанены")
    context = {
        'title': "Вход в аккаунт",
        'form': UserLoginForm
    }
    return render(request, 'users/user_login.html', context=context)


@login_required
def user_profile_view(request):
    user_object = request.user
    if user_object.first_name and user_object.last_name:
        user_name = user_object.first_name + ' ' + user_object.last_name
    else:
        user_name = user_object
    context = {
        'title': f"Ваш профиль: {user_name}"
    }
    return render(request, 'users/user_profile_read_only.html', context=context)


@login_required
def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')