from django.urls import path

from users.apps import UsersConfig
from users.views import (UserRegisterView, UserProfileView, UserLoginView, user_logout_view, UserUpdateView,
                         UserPasswordChangeView, user_generate_new_password_view)
from django.core.exceptions import ValidationError


app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='user_login'),
    path('logout/', user_logout_view, name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change_password/', UserPasswordChangeView.as_view(), name='user_change_password'),
    path('profile/genpassword', user_generate_new_password_view, name='user_generate_new_password')
]