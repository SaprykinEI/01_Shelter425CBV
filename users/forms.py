from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class StyleFormMixin:
    """Миксин для добавления CSS-класса 'form-control' ко всем виджетам формы."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    """Форма для отображения и редактирования профиля пользователя."""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя с проверкой пароля."""
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password1'])
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError(
                self.error_messages['password_missmatch'],
                code='password_missmatch'
            )

        return cleaned_data['password2']


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма входа пользователя."""
    pass


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма обновления данных пользователя."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    """Форма изменения пароля пользователя с валидацией новых паролей."""
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_missmatch'],
                code='password_missmatch'
            )

        password_validation.validate_password(password2, self.user)
        return password2
